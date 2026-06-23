"""Artifact generation — prompts, parsing, streaming."""

from src.artifacts.generator import generate_artifact
from src.artifacts.parser import (
    get_available_commands,
    get_available_files,
    is_slash_command,
    match_files,
    parse_slash_command,
)

__all__ = [
    "generate_artifact",
    "get_available_commands",
    "get_available_files",
    "is_slash_command",
    "match_files",
    "parse_slash_command",
]
