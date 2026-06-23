"""Embedding model wrapper — singleton sentence-transformer instance."""

import logging
from typing import Optional

from sentence_transformers import SentenceTransformer

from src.config import EMBEDDING_MODEL

logger = logging.getLogger(__name__)

_model: Optional[SentenceTransformer] = None


def get_model() -> SentenceTransformer:
    """Return the singleton SentenceTransformer model, loading on first call."""
    global _model
    if _model is None:
        logger.info("Loading embedding model: %s", EMBEDDING_MODEL)
        _model = SentenceTransformer(EMBEDDING_MODEL)
        logger.info("Embedding model loaded (dim=%d)", _model.get_sentence_embedding_dimension())
    return _model


def embed_documents(texts: list[str]) -> list[list[float]]:
    """Embed a list of document texts.

    Args:
        texts: List of text strings to embed.

    Returns:
        List of embedding vectors, one per input text.
    """
    if not texts:
        return []
    model = get_model()
    embeddings = model.encode(texts, show_progress_bar=False, convert_to_numpy=True)
    return embeddings.tolist()


def embed_query(text: str) -> list[float]:
    """Embed a single query string.

    Args:
        text: The query text to embed.

    Returns:
        Embedding vector for the query.
    """
    model = get_model()
    embedding = model.encode([text], show_progress_bar=False, convert_to_numpy=True)
    return embedding[0].tolist()
