"""Data models — structured types used across the application."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class SourceChunk:
    """A single retrieved chunk with source metadata."""

    content: str
    source: str  # filename
    page: int  # page or slide number
    score: float = 0.0  # similarity score

    @property
    def label(self) -> str:
        """Human-readable source label."""
        return f"{self.source} (p. {self.page})"

    def to_dict(self) -> dict[str, Any]:
        """Serialize to dict for JSON storage."""
        return {
            "content": self.content,
            "source": self.source,
            "page": self.page,
            "score": self.score,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SourceChunk":
        """Deserialize from dict."""
        return cls(
            content=data["content"],
            source=data["source"],
            page=data["page"],
            score=data.get("score", 0.0),
        )


@dataclass
class ChatMessage:
    """A single message in a chat session."""

    role: str  # "user" or "assistant"
    content: str
    sources: list[SourceChunk] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> dict[str, Any]:
        """Serialize to dict for JSON storage."""
        return {
            "role": self.role,
            "content": self.content,
            "sources": [s.to_dict() for s in self.sources],
            "timestamp": self.timestamp,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ChatMessage":
        """Deserialize from dict."""
        sources = [SourceChunk.from_dict(s) for s in data.get("sources", [])]
        return cls(
            role=data["role"],
            content=data["content"],
            sources=sources,
            timestamp=data.get("timestamp", ""),
        )


@dataclass
class Session:
    """A chat session containing messages."""

    id: str
    name: str
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    messages: list[ChatMessage] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Serialize to dict for JSON storage."""
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at,
            "messages": [m.to_dict() for m in self.messages],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Session":
        """Deserialize from dict."""
        messages = [ChatMessage.from_dict(m) for m in data.get("messages", [])]
        return cls(
            id=data["id"],
            name=data["name"],
            created_at=data.get("created_at", ""),
            messages=messages,
        )


@dataclass
class Artifact:
    """A generated artifact (summary, glossary, etc.)."""

    id: str
    type: str  # "summary", "glossary", "compare", "explain"
    name: str
    subject: str
    source_file: str = ""
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> dict[str, Any]:
        """Serialize to dict for JSON storage."""
        return {
            "id": self.id,
            "type": self.type,
            "name": self.name,
            "subject": self.subject,
            "source_file": self.source_file,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Artifact":
        """Deserialize from dict."""
        return cls(
            id=data["id"],
            type=data["type"],
            name=data["name"],
            subject=data["subject"],
            source_file=data.get("source_file", ""),
            created_at=data.get("created_at", ""),
        )
