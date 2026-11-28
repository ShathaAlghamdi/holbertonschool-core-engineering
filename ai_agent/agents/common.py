#!/usr/bin/env python3
"""Shared helpers: model configuration and a small agent runner."""
import os
import uuid

from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import InMemoryRunner
from google.genai import types

APP_NAME = "ai-agent"
USER_ID = "student"
DEFAULT_MODEL = "ollama_chat/llama3.2"


def get_model_name():
    """Return the LiteLLM model name from the environment."""
    return os.getenv("MODEL_NAME", DEFAULT_MODEL).strip() or DEFAULT_MODEL


def build_model():
    """Build the LiteLLM model object used by every agent."""
    return LiteLlm(model=get_model_name())


async def run_agent(agent, prompt):
    """Send one prompt to an agent and return its final text answer."""
    runner = InMemoryRunner(agent=agent, app_name=APP_NAME)
    session = await runner.session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=str(uuid.uuid4()),
    )
    message = types.Content(role="user", parts=[types.Part(text=prompt)])

    final_text = ""
    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=session.id,
        new_message=message,
    ):
        if event.is_final_response() and event.content and event.content.parts:
            final_text = "".join(
                part.text or "" for part in event.content.parts
            )
    return final_text.strip()
