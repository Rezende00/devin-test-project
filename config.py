import os

ENABLE_RAG_TOOL = os.getenv("ENABLE_RAG_TOOL", "true").lower() == "true"

USE_GEMINI_1_5_PRO = os.getenv("USE_GEMINI_1_5_PRO", "false").lower() == "true"

ENABLE_SENTIMENT_ANALYSIS = os.getenv("ENABLE_SENTIMENT_ANALYSIS", "true").lower() == "true"

USE_STREAMING_RESPONSE = os.getenv("USE_STREAMING_RESPONSE", "false").lower() == "true"
