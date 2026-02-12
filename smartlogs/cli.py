"""CLI entry point for SmartLogs."""

import click
from dotenv import load_dotenv

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from smartlogs.agent import create_agent
from smartlogs.tools import format_analysis

load_dotenv()

APP_NAME = "smartlogs"
USER_ID = "cli_user"


def run_agent(log_entry: str) -> str:
    """Run the SmartLogs agent on a log entry and return the response."""
    agent = create_agent()
    session_service = InMemorySessionService()
    session = session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
    )

    runner = Runner(
        agent=agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    user_message = types.Content(
        role="user",
        parts=[types.Part(text=f"Analyze this error log:\n\n{log_entry}")],
    )

    final_response = ""
    for event in runner.run(
        user_id=USER_ID,
        session_id=session.id,
        new_message=user_message,
    ):
        if event.is_final_response():
            for part in event.content.parts:
                if part.text:
                    final_response += part.text

    return final_response


@click.group()
@click.version_option(version="0.1.0")
def main():
    """SmartLogs - AI-powered error log analyzer."""
    pass


@main.command()
@click.argument("log_entry")
def analyze(log_entry: str):
    """Analyze a single error log entry.

    Example: smartlogs analyze "ERROR: Connection refused on port 5432"
    """
    click.echo("Analyzing log entry...\n")
    result = run_agent(log_entry)
    click.echo(result)


@main.command()
@click.argument("filepath", type=click.Path(exists=True))
def analyze_file(filepath: str):
    """Analyze error logs from a file (one per line)."""
    with open(filepath, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    click.echo(f"Found {len(lines)} log entries. Analyzing...\n")

    for i, line in enumerate(lines, 1):
        click.echo(f"--- Entry {i}/{len(lines)} ---")
        result = run_agent(line)
        click.echo(result)
        click.echo()


if __name__ == "__main__":
    main()
