# SmartLogs

AI-powered error log analyzer using Google ADK agents.

SmartLogs takes error logs and stack traces, breaks them down with an AI agent, searches for known solutions, and provides actionable fixes — all from the command line.

## Vision

While this is a simple CLI tool today, the architecture is designed to integrate into enterprise workflows:
- **CI/CD pipelines** — analyze build/test failures automatically
- **Observability platforms** — plug into Datadog, Sentry, or similar via API
- **Code quality tools** — pipe SonarQube findings for AI-powered remediation
- **Project-context-aware** — future versions will understand your codebase for more relevant fixes

## Setup

```bash
# Install dependencies
uv sync

# Set your Google API key
export GOOGLE_API_KEY=your_key_here

# Or use a .env file
cp .env.example .env
```

## Usage

```bash
# Analyze a single error log
smartlogs analyze "ERROR: Connection refused on port 5432"

# Analyze logs from a file
smartlogs analyze-file errors.log

# Try with the included sample files
smartlogs analyze-file samples/web_server.log
smartlogs analyze-file samples/kubernetes.log
smartlogs analyze-file samples/python_traceback.log
smartlogs analyze-file samples/java_stacktrace.log
```

## Sample Logs

The `samples/` directory contains realistic log files for testing:

- **web_server.log** — HTTP server logs with slow queries, cache failures, and OOM
- **python_traceback.log** — Python exceptions with full tracebacks
- **kubernetes.log** — K8s pod events, OOMKilled, disk pressure, image pull errors
- **java_stacktrace.log** — Java exceptions with stack traces (NPE, StackOverflow)

## Development

```bash
# Run tests
uv run pytest tests/ -v

# Run with uv
uv run smartlogs analyze "ERROR: timeout waiting for response"
```

## Tech Stack

- **Google ADK** — Agent framework with tool use and search capabilities
- **Click** — CLI interface
- **Gemini** — LLM backend via Google ADK