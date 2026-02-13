# Justfile (for windows)
set windows-shell := ["powershell.exe", "-NoLogo", "-Command"]

# Install dependencies
install:
    uv sync --native-tls

# Run ADK web interface (chatbot UI)
run:
    uv run adk web --no-reload

# Run agent in terminal mode
chat:
    uv run adk run devin_support_agent

# Show project info
info:
    @echo "Devin AI Customer Support Agent - Google ADK + Gemini POC"
    @echo "Available commands:"
    @echo "  just install    - Install dependencies"
    @echo "  just run        - Run ADK web interface (http://localhost:8000)"
    @echo "  just chat       - Run agent in terminal mode"
    @echo ""
    @echo "Web UI will be available at: http://localhost:8000"

# Clean cache
clean:
    uv clean cache

# Default command
default: info
