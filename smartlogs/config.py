"""Configuration and environment handling for SmartLogs."""

import os

from dotenv import load_dotenv

load_dotenv()


def get_google_api_key() -> str:
    """Retrieve Google API key from environment."""
    key = os.environ.get("GOOGLE_API_KEY")
    if not key:
        raise KeyError("GOOGLE_API_KEY not found in environment variables")
    return key


def get_model_name() -> str:
    """Get the model name to use for the agent."""
    return os.environ.get("SMARTLOGS_MODEL", "gemini-2.5-flash")


def get_max_retries() -> int:
    """Get the maximum number of retries for transient API errors."""
    value = os.environ.get("SMARTLOGS_MAX_RETRIES", "3")
    try:
        return max(0, int(value))
    except (ValueError, TypeError):
        return 3
