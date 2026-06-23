"""Chat history persistence — JSON CRUD for sessions."""

import json
import uuid
from pathlib import Path

from src.config import CHAT_HISTORY_DIR
from src.exceptions import SessionNotFoundError
from src.models import ChatMessage, Session, SourceChunk


def _history_path(subject: str) -> Path:
    """Return the JSON file path for a subject's chat history."""
    return CHAT_HISTORY_DIR / f"{subject}.json"


def _read_file(path: Path) -> dict:
    """Read JSON file, return empty structure if missing."""
    if not path.exists():
        return {"sessions": {}}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _write_file(path: Path, data: dict) -> None:
    """Write data to JSON file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_sessions(subject: str) -> dict[str, Session]:
    """Load all sessions for a subject. Returns dict keyed by session ID."""
    data = _read_file(_history_path(subject))
    sessions = {}
    for sid, sdata in data.get("sessions", {}).items():
        sessions[sid] = Session.from_dict(sdata)
    return sessions


def save_sessions(subject: str, sessions: dict[str, Session]) -> None:
    """Save all sessions for a subject, overwriting the file."""
    data = {"sessions": {sid: s.to_dict() for sid, s in sessions.items()}}
    _write_file(_history_path(subject), data)


def create_session(subject: str, name: str = "New Chat") -> str:
    """Create a new empty session and return its ID."""
    sessions = load_sessions(subject)
    sid = str(uuid.uuid4())
    sessions[sid] = Session(id=sid, name=name)
    save_sessions(subject, sessions)
    return sid


def delete_session(subject: str, session_id: str) -> None:
    """Delete a session. Raises SessionNotFoundError if not found."""
    sessions = load_sessions(subject)
    if session_id not in sessions:
        raise SessionNotFoundError(session_id, subject)
    del sessions[session_id]
    save_sessions(subject, sessions)


def rename_session(subject: str, session_id: str, new_name: str) -> None:
    """Rename a session. Raises SessionNotFoundError if not found."""
    sessions = load_sessions(subject)
    if session_id not in sessions:
        raise SessionNotFoundError(session_id, subject)
    sessions[session_id].name = new_name
    save_sessions(subject, sessions)


def add_message(
    subject: str,
    session_id: str,
    role: str,
    content: str,
    sources: list[SourceChunk] | None = None,
) -> None:
    """Add a message to a session. Raises SessionNotFoundError if not found."""
    sessions = load_sessions(subject)
    if session_id not in sessions:
        raise SessionNotFoundError(session_id, subject)
    msg = ChatMessage(role=role, content=content, sources=sources or [])
    sessions[session_id].messages.append(msg)
    save_sessions(subject, sessions)


def auto_name_session(subject: str, session_id: str, first_message: str) -> None:
    """Set session name from the first user message (truncated to 40 chars)."""
    sessions = load_sessions(subject)
    if session_id not in sessions:
        raise SessionNotFoundError(session_id, subject)
    name = first_message.strip()[:40]
    if len(first_message.strip()) > 40:
        name += "..."
    sessions[session_id].name = name
    save_sessions(subject, sessions)
