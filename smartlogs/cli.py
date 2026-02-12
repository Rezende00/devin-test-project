"""CLI entry point for SmartLogs."""

import asyncio
import logging

import click
from dotenv import load_dotenv

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from smartlogs.agent import create_agent
from smartlogs.tools import format_analysis

load_dotenv()

LOG_FORMAT = "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"

APP_NAME = "smartlogs"
USER_ID = "cli_user"

logger = logging.getLogger("smartlogs.cli")


def setup_logging(verbose: bool = False) -> None:
    """Configure logging for SmartLogs."""
    level = logging.DEBUG if verbose else logging.INFO
    root = logging.getLogger()
    root.setLevel(level)
    if not root.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(LOG_FORMAT))
        root.addHandler(handler)
    for handler in root.handlers:
        handler.setFormatter(logging.Formatter(LOG_FORMAT))


async def _run_agent_async(log_entry: str) -> str:
    """Run the SmartLogs agent on a log entry and return the response."""
    agent = create_agent()
    session_service = InMemorySessionService()
    session = await session_service.create_session(
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
    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=session.id,
        new_message=user_message,
    ):
        if event.is_final_response():
            for part in event.content.parts:
                if part.text:
                    final_response += part.text

    return final_response


def run_agent(log_entry: str) -> str:
    """Synchronous wrapper for the async agent runner."""
    return asyncio.run(_run_agent_async(log_entry))


@click.group()
@click.version_option(version="0.1.0")
@click.option("--verbose", "-v", is_flag=True, help="Enable debug logging output.")
@click.pass_context
def main(ctx: click.Context, verbose: bool) -> None:
    """SmartLogs - AI-powered error log analyzer."""
    setup_logging(verbose=verbose)
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose


@main.command()
@click.argument("log_entry")
def analyze(log_entry: str):
    """Analyze a single error log entry.

    Example: smartlogs analyze "ERROR: Connection refused on port 5432"
    """
    logger.info("Analyzing log entry...")
    result = run_agent(log_entry)
    click.echo(result)


@main.command()
@click.argument("filepath", type=click.Path(exists=True))
def analyze_file(filepath: str):
    """Analyze error logs from a file (one per line)."""
    with open(filepath, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    logger.info("Found %d log entries. Analyzing...", len(lines))

    for i, line in enumerate(lines, 1):
        logger.info("--- Entry %d/%d ---", i, len(lines))
        result = run_agent(line)
        click.echo(result)
        click.echo()


if __name__ == "__main__":
    main()
