#!/usr/bin/env python3
"""Explainer Agent: explains a programming topic for beginners."""
from google.adk.agents import Agent

from agents.common import build_model, run_agent

EXPLAINER_INSTRUCTION = """You are an explainer agent for beginner students.
You receive a programming topic. Explain it clearly and briefly.

Return ONLY Markdown using exactly these level-2 headings, in this order:

## Simple Explanation
Two or three short paragraphs in plain words.

## Key Concepts
A bullet list of 3 to 5 key concepts, one short sentence each.

## Example
One small, correct code example in a fenced code block,
followed by one sentence explaining what it does.

## Common Mistakes
A bullet list of 2 or 3 mistakes beginners often make with this topic.

## Final Summary
Two or three sentences that summarise the topic.

Rules:
- Do not add any other headings.
- Do not write an introduction before the first heading.
- Do not create exercises; another agent does that.
- If you are not sure about a detail, leave it out instead of guessing.
"""


def create_explainer_agent():
    """Create the Explainer Agent."""
    return Agent(
        name="explainer_agent",
        model=build_model(),
        description="Explains programming topics clearly for beginners.",
        instruction=EXPLAINER_INSTRUCTION,
    )


async def run_explainer_agent(topic):
    """Run the Explainer Agent on a topic and return Markdown."""
    agent = create_explainer_agent()
    prompt = "Topic: {}".format(topic)
    return await run_agent(agent, prompt)
