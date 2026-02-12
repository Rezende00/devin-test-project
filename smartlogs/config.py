"""Configuration and environment handling for SmartLogs."""

import os

from dotenv import load_dotenv

load_dotenv()


def get_hf_api_key() -> str:
    """Retrieve Hugging Face API key from environment.

    Checks HF_TOKEN first (LiteLLM convention), then HF_API_KEY as fallback.
    """
    key = os.environ.get("HF_TOKEN") or os.environ.get("HF_API_KEY")
    if not key:
        raise KeyError(
            "HF_TOKEN not found in environment variables. "
            "Set HF_TOKEN or HF_API_KEY in your .env file. "
            "Get a token at https://huggingface.co/settings/tokens"
        )
    return key


def get_model_name() -> str:
    """Get the model name to use for the agent.

    Default: Llama-3.3-70B-Instruct via HuggingFace + Sambanova provider.
    Format: huggingface/<provider>/<org>/<model>.
    """
    return os.environ.get(
        "SMARTLOGS_MODEL",
        "huggingface/sambanova/meta-llama/Llama-3.3-70B-Instruct",
    )
