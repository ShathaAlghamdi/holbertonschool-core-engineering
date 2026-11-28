#!/usr/bin/env python3
"""Deterministic tool that checks a study guide's required sections."""
import re

REQUIRED_SECTIONS = [
    "Topic",
    "Simple Explanation",
    "Key Concepts",
    "Example",
    "Practice Exercise",
    "Common Mistakes",
    "Review Comments",
    "Final Summary",
]


def _headings(markdown):
    """Return the set of heading titles (any level) found in Markdown."""
    titles = set()
    for line in markdown.splitlines():
        match = re.match(r"^\s*#{1,6}\s+(.+?)\s*#*\s*$", line)
        if match:
            titles.add(match.group(1).strip().lower())
    return titles


def validate_required_sections(markdown: str) -> dict:
    """Check that every required section exists as a Markdown heading.

    The first heading ("# <topic>") counts as the Topic section.
    Returns {"valid": bool, "missing": [section names]}.
    """
    if not isinstance(markdown, str):
        markdown = ""
    titles = _headings(markdown)
    has_title = bool(re.search(r"^\s*#\s+\S", markdown, re.MULTILINE))

    missing = []
    for section in REQUIRED_SECTIONS:
        if section == "Topic":
            if not has_title and "topic" not in titles:
                missing.append(section)
        elif section.lower() not in titles:
            missing.append(section)

    return {"valid": not missing, "missing": missing}
