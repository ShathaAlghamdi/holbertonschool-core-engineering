#!/usr/bin/env python3
"""AI Study Guide Generator: runs the sequential multi-agent workflow.

Usage:
    python3 main.py "Python decorators"
    python3 main.py            # asks for the topic
"""
import asyncio
import os
import re
import socket
import sys
from urllib.parse import urlparse

from dotenv import load_dotenv

from agents.common import get_model_name
from agents.explainer_agent import run_explainer_agent
from agents.practice_designer_agent import run_practice_designer_agent
from agents.reviewer_agent import run_reviewer_agent
from tools.file_writer import save_markdown_file
from tools.validation import validate_required_sections

OUTPUT_FILE = os.path.join("output", "study_guide.md")
EXPLAINER_SECTIONS = [
    "Simple Explanation",
    "Key Concepts",
    "Example",
    "Common Mistakes",
    "Final Summary",
]


class ConfigError(Exception):
    """Raised when the environment is not configured correctly."""


def get_topic_from_user():
    """Read the topic from the command line or ask for it."""
    if len(sys.argv) > 1:
        topic = " ".join(sys.argv[1:])
    else:
        topic = input("Enter a programming topic: ")
    topic = topic.strip()
    if not topic:
        raise ValueError("Topic cannot be empty.")
    return topic


def check_configuration():
    """Check environment variables and that Ollama is reachable."""
    model = os.getenv("MODEL_NAME", "").strip()
    if not model:
        raise ConfigError(
            "MODEL_NAME is not set. Copy .env.example to .env and set it, "
            "for example MODEL_NAME=ollama_chat/llama3.2"
        )
    if not model.startswith(("ollama/", "ollama_chat/")):
        return  # Another LiteLLM provider: its own key is checked by LiteLLM.

    base = os.getenv("OLLAMA_API_BASE", "").strip()
    if not base:
        raise ConfigError(
            "OLLAMA_API_BASE is not set. Use http://localhost:11434 "
            "in your .env file."
        )
    url = urlparse(base)
    try:
        with socket.create_connection(
            (url.hostname or "localhost", url.port or 11434), timeout=3
        ):
            pass
    except OSError:
        raise ConfigError(
            "Cannot reach Ollama at {}. Start it with 'ollama serve' "
            "(or open the Ollama app) and try again.".format(base)
        )


def split_sections(markdown):
    """Split agent Markdown into {heading: body} using '## ' headings."""
    sections = {}
    current = None
    lines = []
    for line in markdown.splitlines():
        match = re.match(r"^\s*#{2,3}\s+(.+?)\s*#*\s*$", line)
        if match:
            if current:
                sections[current] = "\n".join(lines).strip()
            current = match.group(1).strip().title()
            lines = []
        elif current:
            lines.append(line)
    if current:
        sections[current] = "\n".join(lines).strip()
    return sections


def assemble_markdown(topic, explanation, practice, review=None):
    """Build the study guide Markdown in one place."""
    parts = split_sections(explanation)
    missing_text = "_The explainer agent did not provide this section._"

    def section(name):
        return parts.get(name, missing_text)

    blocks = [
        "# {}".format(topic),
        "## Simple Explanation\n\n" + section("Simple Explanation"),
        "## Key Concepts\n\n" + section("Key Concepts"),
        "## Example\n\n" + section("Example"),
        "## Practice Exercise\n\n" + practice.strip(),
        "## Common Mistakes\n\n" + section("Common Mistakes"),
    ]
    if review is not None:
        blocks.append("## Review Comments\n\n" + review.strip())
    blocks.append("## Final Summary\n\n" + section("Final Summary"))
    return "\n\n".join(blocks) + "\n"


def explain_agent_error(error):
    """Turn common model errors into a readable message."""
    text = str(error)
    lowered = text.lower()
    if "not found" in lowered and "model" in lowered:
        return (
            "The model '{}' is not available. Run 'ollama pull <model>' "
            "and check MODEL_NAME in .env.".format(get_model_name())
        )
    if "connection" in lowered or "refused" in lowered:
        return "The model server is not responding. Is Ollama running?"
    return "The agent failed: {}".format(text)


async def run_workflow(topic):
    """Run every step of the workflow in order and return the Markdown."""
    print("[1/6] Explainer Agent: explaining '{}'...".format(topic))
    explanation = await run_explainer_agent(topic)

    print("[2/6] Practice Designer Agent: creating an exercise...")
    practice = await run_practice_designer_agent(topic, explanation)

    print("[3/6] Assembling the draft study guide...")
    draft = assemble_markdown(topic, explanation, practice)

    print("[4/6] Reviewer Agent: reviewing the draft...")
    review = await run_reviewer_agent(draft)

    print("[5/6] Assembling the final study guide...")
    return assemble_markdown(topic, explanation, practice, review)


def main():
    """Entry point."""
    load_dotenv()
    try:
        topic = get_topic_from_user()
        check_configuration()
    except (ValueError, ConfigError) as error:
        print("Error: {}".format(error), file=sys.stderr)
        return 1

    try:
        final_markdown = asyncio.run(run_workflow(topic))
    except Exception as error:  # Model errors come in many types.
        print("Error: {}".format(explain_agent_error(error)), file=sys.stderr)
        if os.getenv("DEBUG") == "1":
            raise
        return 1

    print("[6/6] Validating and saving...")
    result = validate_required_sections(final_markdown)
    if result["valid"]:
        print("Validation passed: all required sections are present.")
    else:
        print("Validation failed. Missing sections: {}".format(
            ", ".join(result["missing"])))

    try:
        saved_path = save_markdown_file(OUTPUT_FILE, final_markdown)
    except (OSError, ValueError) as error:
        print("Error: {}".format(error), file=sys.stderr)
        return 1

    print("Study guide saved to {}".format(saved_path))
    return 0 if result["valid"] else 2


if __name__ == "__main__":
    sys.exit(main())
