"""Artifact persistence — save, load, list, delete markdown artifacts."""

import re
from pathlib import Path

from src.config import ARTIFACTS_DIR
from src.models import Artifact

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_FRONT_MATTER_RE = re.compile(r"^---\n(.+?)\n---\n", re.DOTALL)


def _artifact_dir(subject: str) -> Path:
    """Return the directory for a subject's artifacts."""
    return ARTIFACTS_DIR / subject


def _artifact_path(artifact: Artifact) -> Path:
    """Return the file path for an artifact."""
    return _artifact_dir(artifact.subject) / f"{artifact.id}.md"


def _build_front_matter(artifact: Artifact) -> str:
    """Build YAML front matter block."""
    return (
        "---\n"
        f"type: {artifact.type}\n"
        f"source_file: {artifact.source_file}\n"
        f"subject: {artifact.subject}\n"
        f"name: {artifact.name}\n"
        f"created_at: {artifact.created_at}\n"
        "---\n\n"
    )


def _parse_front_matter(content: str) -> tuple[dict, str]:
    """Extract YAML front matter and body from markdown content."""
    match = _FRONT_MATTER_RE.match(content)
    if not match:
        return {}, content
    raw_fm = match.group(1)
    body = content[match.end():]
    fm = {}
    for line in raw_fm.strip().splitlines():
        if ":" in line:
            key, val = line.split(":", 1)
            fm[key.strip()] = val.strip()
    return fm, body


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def save_artifact(artifact: Artifact, content: str) -> None:
    """Save an artifact markdown file with YAML front matter."""
    path = _artifact_path(artifact)
    path.parent.mkdir(parents=True, exist_ok=True)
    full = _build_front_matter(artifact) + content
    with open(path, "w", encoding="utf-8") as f:
        f.write(full)


def load_artifact(artifact_id: str, subject: str) -> tuple[Artifact, str] | None:
    """Load an artifact by ID. Returns (artifact, body) or None if not found."""
    path = _artifact_dir(subject) / f"{artifact_id}.md"
    if not path.exists():
        return None
    raw = path.read_text(encoding="utf-8")
    fm, body = _parse_front_matter(raw)
    artifact = Artifact(
        id=artifact_id,
        type=fm.get("type", "unknown"),
        name=fm.get("name", artifact_id),
        subject=fm.get("subject", subject),
        source_file=fm.get("source_file", ""),
        created_at=fm.get("created_at", ""),
    )
    return artifact, body


def list_artifacts(subject: str) -> list[Artifact]:
    """List all artifacts for a subject, sorted by creation time (newest first)."""
    d = _artifact_dir(subject)
    if not d.exists():
        return []
    artifacts = []
    for p in d.glob("*.md"):
        raw = p.read_text(encoding="utf-8")
        fm, _ = _parse_front_matter(raw)
        artifacts.append(
            Artifact(
                id=p.stem,
                type=fm.get("type", "unknown"),
                name=fm.get("name", p.stem),
                subject=fm.get("subject", subject),
                source_file=fm.get("source_file", ""),
                created_at=fm.get("created_at", ""),
            )
        )
    artifacts.sort(key=lambda a: a.created_at, reverse=True)
    return artifacts


def delete_artifact(artifact_id: str, subject: str) -> bool:
    """Delete an artifact file. Returns True if deleted, False if not found."""
    path = _artifact_dir(subject) / f"{artifact_id}.md"
    if not path.exists():
        return False
    path.unlink()
    return True
