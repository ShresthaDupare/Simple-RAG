"""Subject and file scanning — discover subjects and files in data/."""

import logging
from pathlib import Path

from src.config import DATA_DIR, SUPPORTED_EXTENSIONS
from src.exceptions import SubjectNotFoundError

logger = logging.getLogger(__name__)


def scan_subjects() -> list[str]:
    """List all subject folder names in data/.

    Returns:
        Sorted list of subject names (folder names).
    """
    if not DATA_DIR.exists():
        logger.warning("Data directory does not exist: %s", DATA_DIR)
        return []

    subjects = [
        entry.name
        for entry in DATA_DIR.iterdir()
        if entry.is_dir() and not entry.name.startswith(".")
    ]
    return sorted(subjects)


def get_files(subject: str) -> list[Path]:
    """List all supported files in a subject folder.

    Args:
        subject: Name of the subject folder.

    Returns:
        List of file paths for supported file types.

    Raises:
        SubjectNotFoundError: If the subject folder does not exist.
    """
    subject_dir = DATA_DIR / subject
    if not subject_dir.exists():
        raise SubjectNotFoundError(subject)

    files = [
        entry
        for entry in subject_dir.iterdir()
        if entry.is_file() and entry.suffix.lower() in SUPPORTED_EXTENSIONS
    ]
    return sorted(files)


def get_subject_dir(subject: str) -> Path:
    """Get the full path to a subject's data folder.

    Args:
        subject: Name of the subject.

    Returns:
        Path to the subject folder.

    Raises:
        SubjectNotFoundError: If the subject folder does not exist.
    """
    subject_dir = DATA_DIR / subject
    if not subject_dir.exists():
        raise SubjectNotFoundError(subject)
    return subject_dir
