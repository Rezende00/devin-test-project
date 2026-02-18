# Devin AI Customer Support Agent

A POC chatbot that answers questions about **Devin AI** (FAQ, pricing, capabilities, integrations) using **Google ADK + Gemini 2.5 Flash**.

## Features

- **FAQ & Knowledge Base** — curated from official Devin docs
- **Pricing Details** — ACU model, Core/Teams/Enterprise plans
- **Feature & Integration Catalog** — structured tool responses
- **DeepWiki MCP** — live GitHub repo documentation lookup
- **ADK Web UI** — built-in browser chat interface

## Prerequisites

- **Python 3.13+**
- **[UV](https://docs.astral.sh/uv/)** — fast Python package manager
- **[just](https://github.com/casey/just)** — command runner (optional, but recommended)
- **Google API key** — required for Gemini LLM access (see [Getting a Google API Key](#getting-a-google-api-key))

## Getting a Google API Key

1. Go to [Google AI Studio](https://aistudio.google.com/apikey).
2. Sign in with your Google account.
3. Click **Create API Key** and select or create a Google Cloud project.
4. Copy the generated key — you will need it in the setup step below.

## Setup

```bash
git clone https://github.com/Rezende00/devin-test-project.git
cd devin-test-project

cp .env.example .env
# Edit .env and replace the placeholder with your actual Google API key

just install   # Install dependencies with UV
```

## Usage

**Web UI** (recommended):

```bash
just run       # Launch ADK web UI at http://localhost:8000
```

**Terminal mode**:

```bash
just chat      # Interactive terminal chat
```

### Example Prompts

Once the agent is running, try asking:

- "What is Devin and what can it do?"
- "How much does Devin cost? Explain the ACU model."
- "What integrations does Devin support?"
- "What are Devin's best practices?"
- "Tell me about the facebook/react repository" *(uses DeepWiki)*

## Project Structure

```
devin-test-project/
  devin_support_agent/    # ADK agent package
    __init__.py
    agent.py              # Agent + tools + DeepWiki MCP
    knowledge.py          # Devin AI knowledge base
  .env                    # GOOGLE_API_KEY (not committed)
  .env.example            # Template for .env
  pyproject.toml
  Justfile
```

## Tech Stack

- **Google ADK** (Agent Development Kit)
- **Gemini 2.5 Flash** (LLM)
- **DeepWiki MCP** (repo documentation)
- **UV** (dependency management)

## Related Projects

- **[devin-test-dashboard](https://github.com/Rezende00/devin-test-dashboard)** — companion dashboard project
