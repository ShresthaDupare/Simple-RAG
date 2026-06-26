"""Slash command parsing — detect and parse artifact commands from user input."""

import re
from pathlib import Path

from src.loaders.scanner import get_files

_COMMANDS = {"summary", "glossary", "compare", "explain"}

_SLASH_RE = re.compile(r"^/(\w+)\s*(.*)", re.DOTALL)


def parse_slash_command(text: str) -> tuple[str | None, str]:
    """Parse a slash command from user input.

    Args:
        text: Raw user input text.

    Returns:
        Tuple of (command, args) if valid slash command, else (None, "").
        command is one of: summary, glossary, compare, explain.
        args is the remaining text after the command.
    """
    text = text.strip()
    match = _SLASH_RE.match(text)
    if not match:
        return None, ""

    command = match.group(1).lower()
    args = match.group(2).strip()

    if command not in _COMMANDS:
        return None, ""

    return command, args


def is_slash_command(text: str) -> bool:
    """Check if text starts with a valid slash command."""
    command, _ = parse_slash_command(text)
    return command is not None


def get_available_commands() -> list[dict[str, str]]:
    """Return available slash commands with descriptions for autocomplete."""
    return [
        {"command": "/summary", "description": "Generate a condensed summary of a document"},
        {"command": "/glossary", "description": "Extract key terms and definitions as a table"},
        {"command": "/compare", "description": "Compare concepts across documents"},
        {"command": "/explain", "description": "Step-by-step walkthrough of a concept"},
    ]


def get_available_files(subject: str) -> list[str]:
    """List filenames in a subject for autocomplete suggestions.

    Args:
        subject: Subject folder name.

    Returns:
        List of filenames (without path) available in the subject.
    """
    try:
        files = get_files(subject)
        return [f.name for f in files]
    except Exception:
        return []


def match_files(partial: str, available: list[str]) -> list[str]:
    """Fuzzy-match a partial filename against available files.

    Args:
        partial: Partial filename entered by user.
        available: List of available filenames.

    Returns:
        Matching filenames sorted by relevance.
    """
    partial_lower = partial.lower()
    matches = []
    for name in available:
        if partial_lower in name.lower():
            matches.append(name)
    return sorted(matches)
