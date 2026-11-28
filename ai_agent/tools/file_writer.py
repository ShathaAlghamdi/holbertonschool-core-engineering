#!/usr/bin/env python3
"""Deterministic tool that saves Markdown content to a file."""
from pathlib import Path


def save_markdown_file(file_path: str, content: str) -> str:
    """Write Markdown content to file_path and return the saved path.

    The parent directory is created if needed. Raises OSError with a
    readable message if the file cannot be written.
    """
    if not file_path or not file_path.strip():
        raise ValueError("File path cannot be empty.")
    if not isinstance(content, str):
        raise TypeError("Markdown content must be a string.")

    path = Path(file_path)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    except OSError as error:
        raise OSError(
            "Could not write Markdown file '{}': {}".format(path, error)
        ) from error
    return str(path.resolve())
