#!/usr/bin/env python3
"""Read a UTF-8 text file and print its content."""


def read_file(filename=""):
    """Read filename and print its content to stdout."""
    with open(filename, "r", encoding="utf-8") as file:
        print(file.read(), end="")
