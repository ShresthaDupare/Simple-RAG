"""Configuration — environment variables, paths, constants, defaults."""

import hashlib
import os
from pathlib import Path

from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Environment
# ---------------------------------------------------------------------------

load_dotenv()

DEEPSEEK_API_KEY: str = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_BASE_URL: str = "https://api.deepseek.com"
DEEPSEEK_MODEL: str = "deepseek-chat"

# ---------------------------------------------------------------------------
# Paths (relative to project root)
# ---------------------------------------------------------------------------

BASE_DIR: Path = Path(__file__).resolve().parent.parent
DATA_DIR: Path = BASE_DIR / "data"
FAISS_DIR: Path = BASE_DIR / "faiss_index"
CHAT_HISTORY_DIR: Path = BASE_DIR / "chat_history"
ARTIFACTS_DIR: Path = BASE_DIR / "artifacts"

# ---------------------------------------------------------------------------
# Supported file types
# ---------------------------------------------------------------------------

SUPPORTED_EXTENSIONS: set[str] = {".pdf", ".pptx"}

# ---------------------------------------------------------------------------
# Default settings (overridable via sidebar sliders)
# ---------------------------------------------------------------------------

DEFAULT_TOP_K: int = 4
DEFAULT_MAX_HISTORY: int = 5
DEFAULT_TEMPERATURE: float = 0.3
DEFAULT_CHUNK_SIZE: int = 1000
DEFAULT_CHUNK_OVERLAP: int = 200

# Slider ranges
TOP_K_RANGE: tuple[int, int] = (1, 10)
MAX_HISTORY_RANGE: tuple[int, int] = (1, 20)
TEMPERATURE_RANGE: tuple[float, float] = (0.0, 1.0)
CHUNK_SIZE_RANGE: tuple[int, int] = (500, 2000)
CHUNK_OVERLAP_RANGE: tuple[int, int] = (50, 500)

# ---------------------------------------------------------------------------
# Embedding model
# ---------------------------------------------------------------------------

EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"

# ---------------------------------------------------------------------------
# Subject colors for sidebar dots
# ---------------------------------------------------------------------------

SUBJECT_COLORS: list[str] = [
    "#6366f1",  # indigo
    "#ec4899",  # pink
    "#f59e0b",  # amber
    "#10b981",  # emerald
    "#3b82f6",  # blue
    "#8b5cf6",  # violet
    "#ef4444",  # red
    "#06b6d4",  # cyan
    "#84cc16",  # lime
    "#f97316",  # orange
]


def get_subject_color(subject_name: str) -> str:
    """Return a consistent color for a subject based on its name."""
    digest = hashlib.md5(subject_name.encode()).hexdigest()
    index = int(digest, 16) % len(SUBJECT_COLORS)
    return SUBJECT_COLORS[index]


# ---------------------------------------------------------------------------
# Ensure directories exist
# ---------------------------------------------------------------------------


def ensure_dirs() -> None:
    """Create all required directories if they don't exist."""
    for directory in (DATA_DIR, FAISS_DIR, CHAT_HISTORY_DIR, ARTIFACTS_DIR):
        directory.mkdir(parents=True, exist_ok=True)


ensure_dirs()
