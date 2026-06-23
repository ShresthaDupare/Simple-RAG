"""FAISS vector store — create, load, search, and manage per-subject indices."""

import json
import logging
import pickle
from pathlib import Path

import faiss
import numpy as np

from src.config import FAISS_DIR
from src.exceptions import IndexNotFoundError
from src.models import SourceChunk
from src.retrieval.embeddings import embed_documents, embed_query

logger = logging.getLogger(__name__)

# File names for persisted index data
_INDEX_FILE = "index.faiss"
_META_FILE = "metadata.pkl"


def _index_dir(subject: str) -> Path:
    """Return the index directory for a subject."""
    return FAISS_DIR / subject


def _ensure_index_dir(subject: str) -> Path:
    """Create and return the index directory for a subject."""
    d = _index_dir(subject)
    d.mkdir(parents=True, exist_ok=True)
    return d


# ---------------------------------------------------------------------------
# CRUD
# ---------------------------------------------------------------------------

def index_exists(subject: str) -> bool:
    """Check whether a FAISS index exists for the given subject."""
    d = _index_dir(subject)
    return (d / _INDEX_FILE).exists() and (d / _META_FILE).exists()


def create_index(
    subject: str,
    chunks: list[SourceChunk],
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
) -> int:
    """Build a FAISS index from chunks and persist to disk.

    Args:
        subject: Subject name (determines the subfolder under faiss_index/).
        chunks: List of SourceChunk objects to index.
        chunk_size: Stored for reference (not used at index time).
        chunk_overlap: Stored for reference (not used at index time).

    Returns:
        Number of vectors indexed.

    Raises:
        ValueError: If chunks list is empty.
    """
    if not chunks:
        raise ValueError("Cannot create index from empty chunk list")

    d = _ensure_index_dir(subject)
    texts = [c.content for c in chunks]
    embeddings = np.array(embed_documents(texts), dtype=np.float32)

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    # Persist
    faiss.write_index(index, str(d / _INDEX_FILE))
    with open(d / _META_FILE, "wb") as f:
        pickle.dump(chunks, f)

    logger.info("Created index for '%s': %d vectors (dim=%d)", subject, len(chunks), dim)
    return len(chunks)


def load_index(subject: str) -> tuple[faiss.Index, list[SourceChunk]]:
    """Load a FAISS index and its metadata from disk.

    Args:
        subject: Subject name.

    Returns:
        Tuple of (FAISS index, list of SourceChunk).

    Raises:
        IndexNotFoundError: If no index exists for the subject.
    """
    d = _index_dir(subject)
    index_path = d / _INDEX_FILE
    meta_path = d / _META_FILE

    if not index_path.exists() or not meta_path.exists():
        raise IndexNotFoundError(subject)

    index = faiss.read_index(str(index_path))
    with open(meta_path, "rb") as f:
        chunks: list[SourceChunk] = pickle.load(f)  # noqa: S301

    logger.info("Loaded index for '%s': %d vectors", subject, index.ntotal)
    return index, chunks


def delete_index(subject: str) -> bool:
    """Delete the index files for a subject.

    Args:
        subject: Subject name.

    Returns:
        True if files were deleted, False if index didn't exist.
    """
    d = _index_dir(subject)
    deleted = False
    for fname in (_INDEX_FILE, _META_FILE):
        p = d / fname
        if p.exists():
            p.unlink()
            deleted = True
    if deleted:
        logger.info("Deleted index for '%s'", subject)
    return deleted


# ---------------------------------------------------------------------------
# Search
# ---------------------------------------------------------------------------

def search(subject: str, query: str, top_k: int = 4) -> list[SourceChunk]:
    """Search within a single subject's index.

    Args:
        subject: Subject name.
        query: Query text.
        top_k: Number of results to return.

    Returns:
        List of SourceChunk sorted by relevance (closest first).

    Raises:
        IndexNotFoundError: If no index exists for the subject.
    """
    index, chunks = load_index(subject)
    query_vec = np.array([embed_query(query)], dtype=np.float32)

    k = min(top_k, index.ntotal)
    distances, indices = index.search(query_vec, k)

    results: list[SourceChunk] = []
    for dist, idx in zip(distances[0], indices[0]):
        if idx < 0:
            continue
        chunk = SourceChunk(
            content=chunks[idx].content,
            source=chunks[idx].source,
            page=chunks[idx].page,
            score=float(1.0 / (1.0 + dist)),  # convert L2 distance to similarity
        )
        results.append(chunk)

    logger.debug("Search '%s' for '%s' -> %d results", subject, query, len(results))
    return results


def search_all(query: str, top_k: int = 4) -> list[SourceChunk]:
    """Search across all subject indices and merge results by score.

    Args:
        query: Query text.
        top_k: Number of results to return per subject (total may be higher).

    Returns:
        Merged list of SourceChunk sorted by score (best first), limited to top_k.
    """
    query_vec = np.array([embed_query(query)], dtype=np.float32)
    all_results: list[SourceChunk] = []

    for subject_dir in FAISS_DIR.iterdir():
        if not subject_dir.is_dir():
            continue
        subject = subject_dir.name
        try:
            index, chunks = load_index(subject)
        except IndexNotFoundError:
            continue

        k = min(top_k, index.ntotal)
        distances, indices = index.search(query_vec, k)

        for dist, idx in zip(distances[0], indices[0]):
            if idx < 0:
                continue
            chunk = SourceChunk(
                content=chunks[idx].content,
                source=chunks[idx].source,
                page=chunks[idx].page,
                score=float(1.0 / (1.0 + dist)),
            )
            all_results.append(chunk)

    all_results.sort(key=lambda c: c.score, reverse=True)
    results = all_results[:top_k]

    logger.debug("Search all for '%s' -> %d results (from %d total)", query, len(results), len(all_results))
    return results
