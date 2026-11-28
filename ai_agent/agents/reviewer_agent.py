#!/usr/bin/env python3
"""Reviewer Agent: reviews a draft study guide and comments on it."""
from google.adk.agents import Agent

from agents.common import build_model, run_agent

REVIEWER_INSTRUCTION = """You are a reviewer agent.
Review the draft study guide for clarity, completeness, and usefulness.
Do not rewrite the guide and do not add headings.

Be specific. "Improve the explanation" is too vague;
"The example does not show the function call" is useful.

Return ONLY this Markdown (bold labels, no headings):

**Missing information:**
- ...

**Unclear or ambiguous parts:**
- ...

**Suggestions:**
- ...

**Recommendation:** Approved, or Needs revision, followed by one short reason.
"""


def create_reviewer_agent():
    """Create the Reviewer Agent."""
    return Agent(
        name="reviewer_agent",
        model=build_model(),
        description="Reviews study guide drafts and gives short feedback.",
        instruction=REVIEWER_INSTRUCTION,
    )


async def run_reviewer_agent(draft):
    """Run the Reviewer Agent on a draft study guide."""
    agent = create_reviewer_agent()
    prompt = "Draft study guide to review:\n\n{}".format(draft)
    return await run_agent(agent, prompt)
