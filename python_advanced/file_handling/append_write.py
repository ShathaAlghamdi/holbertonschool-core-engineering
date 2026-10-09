#!/usr/bin/env python3
"""Append text to a UTF-8 file."""


def append_write(filename="", text=""):
    """Append text to filename and return characters added."""
    with open(filename, "a", encoding="utf-8") as file:
        return file.write(text)
