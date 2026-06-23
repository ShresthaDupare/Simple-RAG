"""PDF document loader — extract pages as text with metadata."""

import logging
from pathlib import Path

from pypdf import PdfReader

from src.exceptions import DocumentLoadError
from src.models import SourceChunk

logger = logging.getLogger(__name__)


def load_pdf(path: Path) -> list[SourceChunk]:
    """Load a PDF file and return pages as SourceChunks.

    Args:
        path: Path to the PDF file.

    Returns:
        List of SourceChunk, one per page.

    Raises:
        DocumentLoadError: If the PDF cannot be read.
    """
    try:
        reader = PdfReader(str(path))
        chunks: list[SourceChunk] = []

        for page_num, page in enumerate(reader.pages, start=1):
            text = page.extract_text()
            if text and text.strip():
                chunks.append(
                    SourceChunk(
                        content=text.strip(),
                        source=path.name,
                        page=page_num,
                    )
                )

        logger.info("Loaded %d pages from %s", len(chunks), path.name)
        return chunks

    except Exception as e:
        raise DocumentLoadError(str(path), str(e)) from e


def load_full_pdf(path: Path) -> str:
    """Load entire PDF as a single text string (for artifacts).

    Args:
        path: Path to the PDF file.

    Returns:
        Full text content of all pages.

    Raises:
        DocumentLoadError: If the PDF cannot be read.
    """
    try:
        reader = PdfReader(str(path))
        pages = []

        for page in reader.pages:
            text = page.extract_text()
            if text and text.strip():
                pages.append(text.strip())

        return "\n\n".join(pages)

    except Exception as e:
        raise DocumentLoadError(str(path), str(e)) from e
