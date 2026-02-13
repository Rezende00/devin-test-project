# Devin AI Customer Support Agent

A POC chatbot that answers questions about **Devin AI** (FAQ, pricing, capabilities, integrations) using **Google ADK + Gemini 2.5 Flash**.

## Features

- **FAQ & Knowledge Base** — curated from official Devin docs
- **Pricing Details** — ACU model, Core/Teams/Enterprise plans
- **Feature & Integration Catalog** — structured tool responses
- **DeepWiki MCP** — live GitHub repo documentation lookup
- **ADK Web UI** — built-in browser chat interface

## Quick Start

```bash
just install   # Install dependencies with UV
just run       # Launch ADK web UI at http://localhost:8000
```

## Project Structure

```
devin-test-project/
  devin_support_agent/    # ADK agent package
    __init__.py
    agent.py              # Agent + tools + DeepWiki MCP
    knowledge.py          # Devin AI knowledge base
  .env                    # GOOGLE_API_KEY
  pyproject.toml
  Justfile
```

## Tech Stack

- **Google ADK** (Agent Development Kit)
- **Gemini 2.5 Flash** (LLM)
- **DeepWiki MCP** (repo documentation)
- **UV** (dependency management)