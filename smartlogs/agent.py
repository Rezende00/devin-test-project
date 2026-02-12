"""Google ADK agent definition for SmartLogs."""

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

from smartlogs.config import get_hf_api_key, get_model_name
from smartlogs.tools import parse_log, classify_severity, format_analysis


AGENT_INSTRUCTION = """You are SmartLogs, an AI-powered error log analyzer.

When given a log entry or error message, you must:
1. Use the parse_log tool to extract structured information from the log
2. Use the classify_severity tool to determine the severity level
3. Provide a detailed analysis including:
   - Error type classification
   - Root cause hypothesis
   - Step-by-step suggested fixes
   - References to relevant documentation or known solutions

Always be concise but thorough. Prioritize actionable fixes.
Format your final response clearly with sections for each part of the analysis.
"""


def create_agent() -> Agent:
    """Create and return the SmartLogs analysis agent."""
    model_name = get_model_name()
    api_key = get_hf_api_key()

    model = LiteLlm(model=model_name, api_key=api_key)

    agent = Agent(
        name="smartlogs_analyzer",
        model=model,
        instruction=AGENT_INSTRUCTION,
        description="Analyzes error logs and provides root cause analysis with suggested fixes",
        tools=[
            parse_log,
            classify_severity,
        ],
    )
    return agent
