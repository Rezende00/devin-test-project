# devin-test-project

A Customer Support Agent built with Google ADK (Agent Development Kit) for the ShopEasy e-commerce platform.

This repository serves as a **target/patient application** for demonstrating autonomous software maintenance using the Devin API.

## Structure

```
devin-test-project/
├── config.py                          # Feature flags configuration
├── customer_support_agent/
│   ├── __init__.py
│   ├── agent.py                       # Main agent definition
│   ├── tools.py                       # Tool definitions
│   └── prompts.py                     # Agent instructions
├── tests/
│   ├── test_tools.py                  # Tool unit tests
│   └── test_agent.py                  # Agent creation tests
├── requirements.txt
└── .env.example
```

## Feature Flags

| Flag | Default | Description |
|------|---------|-------------|
| `ENABLE_RAG_TOOL` | `true` | Enables RAG-based knowledge retrieval tool |
| `USE_GEMINI_1_5_PRO` | `false` | Switches model from gemini-2.0-flash to gemini-1.5-pro |
| `ENABLE_SENTIMENT_ANALYSIS` | `true` | Enables customer sentiment analysis |
| `USE_STREAMING_RESPONSE` | `false` | Enables streaming response mode |

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your Google API key
```

## Testing

```bash
pytest tests/ -v
```

## Known Issues

This project intentionally contains bugs for demonstration purposes. See the GitHub Issues tab for details.
