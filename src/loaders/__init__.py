"""Document loaders — PDF, PPTX, and subject scanning.

Provides a unified interface for loading documents regardless of format.
"""

import logging
from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.config import DEFAULT_CHUNK_OVERLAP, DEFAULT_CHUNK_SIZE
from src.exceptions import DocumentLoadError
from src.loaders.pdf_loader import load_full_pdf, load_pdf
from src.loaders.pptx_loader import load_full_pptx, load_pptx
from src.loaders.scanner import get_files, get_subject_dir, scan_subjects
from src.models import SourceChunk

logger = logging.getLogger(__name__)

# Re-export scanner functions for convenience
__all__ = [
    "scan_subjects",
    "get_files",
    "get_subject_dir",
    "load_document",
    "load_and_chunk",
    "load_full_document",
]


def load_document(path: Path) -> list[SourceChunk]:
    """Load a document and return chunks with metadata.

    Dispatches to the appropriate loader based on file extension.

    Args:
        path: Path to the document file.

    Returns:
        List of SourceChunk with content and metadata.

    Raises:
        DocumentLoadError: If the file type is unsupported or loading fails.
    """
    suffix = path.suffix.lower()

    if suffix == ".pdf":
        return load_pdf(path)
    elif suffix == ".pptx":
        return load_pptx(path)
    else:
        raise DocumentLoadError(str(path), f"Unsupported file type: {suffix}")


def load_full_document(path: Path) -> str:
    """Load entire document as a single text string (for artifacts).

    Args:
        path: Path to the document file.

    Returns:
        Full text content of the document.
    """
    suffix = path.suffix.lower()

    if suffix == ".pdf":
        return load_full_pdf(path)
    elif suffix == ".pptx":
        return load_full_pptx(path)
    else:
        raise DocumentLoadError(str(path), f"Unsupported file type: {suffix}")


def load_and_chunk(
    subject: str,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
) -> list[SourceChunk]:
    """Load all files for a subject and split into chunks.

    Args:
        subject: Name of the subject folder.
        chunk_size: Maximum characters per chunk.
        chunk_overlap: Overlap between consecutive chunks.

    Returns:
        List of SourceChunk from all files in the subject.
    """
    files = get_files(subject)
    all_chunks: list[SourceChunk] = []
    failed_files: list[str] = []

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    for file_path in files:
        try:
            chunks = load_document(file_path)
            for chunk in chunks:
                # Split long text while preserving metadata
                texts = splitter.split_text(chunk.content)
                for i, text in enumerate(texts):
                    all_chunks.append(
                        SourceChunk(
                            content=text,
                            source=chunk.source,
                            page=chunk.page,
                        )
                    )
        except Exception as e:
            logger.error("Failed to load %s: %s", file_path, e)
            failed_files.append(file_path.name)
            continue

    if failed_files:
        logger.warning(
            "Failed to load %d/%d files in '%s': %s",
            len(failed_files), len(files), subject, ", ".join(failed_files),
        )

    logger.info("Loaded %d chunks from %d files in '%s'", len(all_chunks), len(files) - len(failed_files), subject)
    return all_chunks
