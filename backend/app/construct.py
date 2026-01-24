"""Dependency injection - service instantiation."""

import os
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables BEFORE importing langsmith (it reads env vars at import time)
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(env_path)

# Also try backend/.env if parent .env doesn't exist
if not env_path.exists():
    backend_env = Path(__file__).parent.parent / ".env"
    load_dotenv(backend_env)

from langsmith.wrappers import wrap_openai  # noqa: E402
from openai import OpenAI  # noqa: E402

from app.services.ai_service import AIService  # noqa: E402
from app.services.state_service import StateService  # noqa: E402


def get_openrouter_api_key() -> str:
    """Get OpenRouter API key from environment.

    Returns:
        OpenRouter API key.

    Raises:
        ValueError: If API key is not set.
    """
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY environment variable is not set")
    return api_key


# Create OpenRouter client for chat completions (wrapped for Langsmith tracing)
openrouter_client = wrap_openai(
    OpenAI(
        api_key=get_openrouter_api_key(),
        base_url="https://openrouter.ai/api/v1",
    )
)

# Create services (singletons)
state_service = StateService(db_path="fact_cards.db")
ai_service = AIService(openrouter_client=openrouter_client)
