"""Dependency injection - service instantiation."""

import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from app.database import Database
from app.services.ai_service import AIService
from app.services.card_service import CardService
from app.services.embedding_service import EmbeddingService

# Load environment variables from parent directory's .env file
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(env_path)

# Also try backend/.env if parent .env doesn't exist
if not env_path.exists():
    backend_env = Path(__file__).parent.parent / ".env"
    load_dotenv(backend_env)


def get_openai_api_key() -> str:
    """Get OpenAI API key from environment.

    Returns:
        OpenAI API key.

    Raises:
        ValueError: If API key is not set.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")
    return api_key


# Create OpenAI client
openai_client = OpenAI(api_key=get_openai_api_key())

# Create database
database = Database(db_path="fact_cards.db")

# Create services
embedding_service = EmbeddingService(openai_client=openai_client)
ai_service = AIService(openai_client=openai_client)
card_service = CardService(database=database, embedding_service=embedding_service)
