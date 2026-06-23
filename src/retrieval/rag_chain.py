"""RAG chain — prompt construction, DeepSeek streaming, and answer generation."""

import logging
from collections.abc import Generator

from openai import OpenAI

from src.config import (
    DEFAULT_MAX_HISTORY,
    DEFAULT_TEMPERATURE,
    DEFAULT_TOP_K,
    DEEPSEEK_API_KEY,
    DEEPSEEK_BASE_URL,
    DEEPSEEK_MODEL,
)
from src.exceptions import APIError, IndexNotFoundError
from src.models import ChatMessage, SourceChunk
from src.retrieval.vector_store import search, search_all

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# System prompt
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """You are a helpful study assistant. You answer questions based on the provided course materials.

Rules:
- Only use information from the provided context to answer.
- If the context does not contain enough information, say so clearly.
- Cite your sources using numbered references like [1], [2], etc.
- Be concise but thorough.
- Use Markdown formatting for clarity (headers, lists, bold).
- If multiple sources are relevant, synthesize information from all of them."""

# ---------------------------------------------------------------------------
# Prompt building
# ---------------------------------------------------------------------------


def _format_sources(chunks: list[SourceChunk]) -> str:
    """Format retrieved chunks into numbered context blocks."""
    if not chunks:
        return "No relevant context found."
    blocks: list[str] = []
    for i, chunk in enumerate(chunks, 1):
        blocks.append(f"[Source {i}] {chunk.label}\n{chunk.content}")
    return "\n\n".join(blocks)


def _format_history(history: list[ChatMessage], max_turns: int) -> str:
    """Format recent chat history into a readable string."""
    if not history:
        return ""
    recent = history[-(max_turns * 2) :]
    lines: list[str] = []
    for msg in recent:
        role = "User" if msg.role == "user" else "Assistant"
        lines.append(f"{role}: {msg.content}")
    return "\n".join(lines)


def build_prompt(
    question: str,
    context_chunks: list[SourceChunk],
    chat_history: list[ChatMessage],
    max_history: int = DEFAULT_MAX_HISTORY,
) -> list[dict[str, str]]:
    """Build the full message list for the LLM call.

    Args:
        question: User's question.
        context_chunks: Retrieved chunks from vector search.
        chat_history: Previous messages in the session.
        max_history: Max number of history turns to include.

    Returns:
        List of message dicts (role + content) for the OpenAI API.
    """
    context_text = _format_sources(context_chunks)
    history_text = _format_history(chat_history, max_history)

    user_content = f"""## Context from Study Materials

{context_text}

---

## Conversation History

{history_text if history_text else "(No prior conversation)"}

---

## Question

{question}"""

    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_content},
    ]


# ---------------------------------------------------------------------------
# DeepSeek streaming
# ---------------------------------------------------------------------------


def get_client() -> OpenAI:
    """Create an OpenAI-compatible client for DeepSeek."""
    if not DEEPSEEK_API_KEY or DEEPSEEK_API_KEY.startswith("sk-your"):
        raise APIError(
            "DeepSeek API key is not configured. "
            "Set DEEPSEEK_API_KEY in your .env file."
        )
    return OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)


def call_deepseek_stream(
    messages: list[dict[str, str]],
    temperature: float = DEFAULT_TEMPERATURE,
) -> Generator[str, None, None]:
    """Stream a response from DeepSeek.

    Args:
        messages: List of message dicts for the API.
        temperature: Sampling temperature.

    Yields:
        Response text tokens as they arrive.

    Raises:
        APIError: If the API call fails.
    """
    client = get_client()

    try:
        stream = client.chat.completions.create(
            model=DEEPSEEK_MODEL,
            messages=messages,
            temperature=temperature,
            stream=True,
        )
        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
    except Exception as e:
        logger.error("DeepSeek API error: %s", e)
        raise APIError(f"DeepSeek API request failed: {e}") from e


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------


def get_answer(
    question: str,
    subject: str | None = None,
    chat_history: list[ChatMessage] | None = None,
    top_k: int = DEFAULT_TOP_K,
    max_history: int = DEFAULT_MAX_HISTORY,
    temperature: float = DEFAULT_TEMPERATURE,
    search_all_subjects: bool = False,
) -> Generator[tuple[str, list[SourceChunk]], None, None]:
    """Generate an answer to a question using RAG.

    Retrieves relevant chunks, builds the prompt, and streams the response.

    Args:
        question: User's question.
        subject: Subject to search within (ignored if search_all_subjects=True).
        chat_history: Previous messages for context.
        top_k: Number of chunks to retrieve.
        max_history: Max history turns to include in prompt.
        temperature: LLM sampling temperature.
        search_all_subjects: If True, search across all subjects.

    Yields:
        Tuples of (text_token, source_chunks). The source_chunks are only
        non-empty on the first yield.

    Raises:
        IndexNotFoundError: If no index exists for the requested subject.
        APIError: If the DeepSeek API call fails.
    """
    if chat_history is None:
        chat_history = []

    # Retrieve relevant chunks
    if search_all_subjects:
        chunks = search_all(question, top_k=top_k)
    else:
        if subject is None:
            raise ValueError("subject is required when search_all_subjects is False")
        chunks = search(subject, question, top_k=top_k)

    # Build prompt
    messages = build_prompt(question, chunks, chat_history, max_history)

    # Stream response — yield chunks on first call, then tokens
    first = True
    for token in call_deepseek_stream(messages, temperature):
        if first:
            yield token, chunks
            first = False
        else:
            yield token, []

    if first:
        # No tokens yielded at all — return empty response with sources
        yield "", chunks
