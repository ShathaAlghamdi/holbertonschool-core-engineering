#!/usr/bin/env python3
"""Practice Designer Agent: creates a small exercise for a topic."""
from google.adk.agents import Agent

from agents.common import build_model, run_agent

PRACTICE_INSTRUCTION = """You are a practice designer agent.
Your task is to create ONE short, beginner-friendly exercise based on the
topic and the explanation you receive.

Do not rewrite the explanation. Do not add any headings.
The exercise must be doable in 10 to 20 minutes, with no external services.

Return ONLY this Markdown (bold labels, no headings):

**Exercise:** what the student must build or do.

**Expected input:** example input, or "Not applicable".

**Expected output:** example output, or "Not applicable".

**Hints:**
- first hint
- second hint (optional)
"""


def create_practice_designer_agent():
    """Create the Practice Designer Agent."""
    return Agent(
        name="practice_designer_agent",
        model=build_model(),
        description="Designs small practice exercises from an explanation.",
        instruction=PRACTICE_INSTRUCTION,
    )


async def run_practice_designer_agent(topic, explanation):
    """Run the Practice Designer Agent using the previous explanation."""
    agent = create_practice_designer_agent()
    prompt = (
        "Topic: {}\n\n"
        "Explanation written by the explainer agent:\n{}\n"
    ).format(topic, explanation)
    return await run_agent(agent, prompt)
