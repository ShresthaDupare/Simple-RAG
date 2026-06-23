"""Retrieval components — embeddings, vector store, RAG chain."""

from src.retrieval.embeddings import embed_documents, embed_query, get_model
from src.retrieval.vector_store import (
    create_index,
    delete_index,
    index_exists,
    load_index,
    search,
    search_all,
)

__all__ = [
    "get_model",
    "embed_documents",
    "embed_query",
    "create_index",
    "load_index",
    "index_exists",
    "delete_index",
    "search",
    "search_all",
]
