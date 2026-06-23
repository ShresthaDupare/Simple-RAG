"""Artifact generator — streaming artifact creation via DeepSeek."""

import logging
import uuid
from collections.abc import Generator

from src.artifacts.prompts import ARTIFACT_PROMPTS, SYSTEM_PROMPT
from src.config import DEFAULT_TEMPERATURE
from src.exceptions import APIError, DocumentLoadError
from src.loaders import get_files, load_full_document
from src.models import Artifact
from src.retrieval.rag_chain import get_client, call_deepseek_stream
from src.retrieval.vector_store import search
from src.storage.artifact_store import save_artifact

logger = logging.getLogger(__name__)


def _build_prompt(
    artifact_type: str,
    content: str,
    topic: str = "",
) -> list[dict[str, str]]:
    """Build the message list for artifact generation."""
    template = ARTIFACT_PROMPTS.get(artifact_type)
    if not template:
        raise ValueError(f"Unknown artifact type: {artifact_type}")

    formatted = template.format(content=content, topic=topic)

    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": formatted},
    ]


def _load_source_content(
    artifact_type: str,
    source_file: str,
    subject: str,
    topic: str,
) -> str:
    """Load document content or retrieve chunks for the artifact."""
    if artifact_type in ("summary", "glossary"):
        # Load full document text
        files = get_files(subject)
        target = None
        for f in files:
            if f.name == source_file:
                target = f
                break
        if target is None:
            raise DocumentLoadError(source_file, f"File not found in subject: {subject}")
        return load_full_document(target)

    elif artifact_type in ("compare", "explain"):
        # Retrieve relevant chunks by topic
        chunks = search(subject, topic, top_k=8)
        if not chunks:
            return f"No relevant content found for topic: {topic}"
        return "\n\n".join(c.content for c in chunks)

    raise ValueError(f"Unknown artifact type: {artifact_type}")


def generate_artifact(
    artifact_type: str,
    source_file: str,
    subject: str,
    topic: str = "",
    temperature: float = DEFAULT_TEMPERATURE,
) -> Generator[tuple[str, Artifact], None, None]:
    """Generate an artifact and stream the content.

    Args:
        artifact_type: One of summary, glossary, compare, explain.
        source_file: Filename to summarize/gloss (for summary/glossary).
        subject: Subject folder name.
        topic: Topic for compare/explain commands.
        temperature: LLM sampling temperature.

    Yields:
        Tuples of (token_text, artifact_metadata). The artifact is yielded
        on the first call so the caller can set up storage/display.

    Raises:
        ValueError: If artifact_type is unknown.
        DocumentLoadError: If source file cannot be loaded.
        APIError: If the DeepSeek API call fails.
    """
    content = _load_source_content(artifact_type, source_file, subject, topic)
    messages = _build_prompt(artifact_type, content, topic)

    # Determine a readable name
    type_label = artifact_type.capitalize()
    if artifact_type in ("summary", "glossary"):
        name = f"{type_label}: {source_file}"
    else:
        name = f"{type_label}: {topic}" if topic else type_label

    artifact = Artifact(
        id=str(uuid.uuid4()),
        type=artifact_type,
        name=name,
        subject=subject,
        source_file=source_file if artifact_type in ("summary", "glossary") else "",
    )

    first = True
    full_text = ""
    for token in call_deepseek_stream(messages, temperature):
        full_text += token
        if first:
            yield token, artifact
            first = False
        else:
            yield token, artifact

    # Save the completed artifact
    if full_text:
        save_artifact(artifact, full_text)
        logger.info("Artifact saved: %s (%s)", artifact.name, artifact_type)
