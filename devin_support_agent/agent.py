"""Devin AI Customer Support Agent — Google ADK + Gemini."""

import httpx

from google.adk.agents import Agent

from . import knowledge


def get_pricing_details() -> dict:
    """Returns detailed pricing information about Devin AI plans and ACU costs.

    Use this tool when the user asks about pricing, plans, costs,
    ACUs (Agent Compute Units), billing, or subscription details.

    Returns:
        dict: Complete pricing information including plans, ACU costs, and tips.
    """
    return {
        "status": "success",
        "pricing": knowledge.PRICING_INFO,
    }


def get_feature_list() -> dict:
    """Returns the categorized list of Devin AI features and capabilities.

    Use this tool when the user asks about what Devin can do, its features,
    capabilities, tools, or specific product functionality.

    Returns:
        dict: Categorized feature list.
    """
    return {
        "status": "success",
        "features": knowledge.FEATURES,
    }


def get_integration_list() -> dict:
    """Returns the list of supported integrations for Devin AI.

    Use this tool when the user asks about integrations, supported platforms,
    connecting Devin to other tools like Slack, GitHub, Jira, etc.

    Returns:
        dict: List of integrations with descriptions.
    """
    return {
        "status": "success",
        "integrations": knowledge.INTEGRATIONS,
    }


def get_faq() -> dict:
    """Returns frequently asked questions and answers about Devin AI.

    Use this tool when the user has common questions about getting started,
    language support, security, API, CI/CD, playbooks, sessions, or DeepWiki.

    Returns:
        dict: List of FAQ items with questions and answers.
    """
    return {
        "status": "success",
        "faq": knowledge.COMMON_ISSUES_FAQ,
    }


def deepwiki_ask(repo_name: str, question: str) -> dict:
    """Ask a question about a public GitHub repository using DeepWiki.

    Use this tool when the user asks about a specific GitHub repository,
    its code, architecture, documentation, or how it works.
    DeepWiki provides AI-powered documentation for GitHub repos.

    Args:
        repo_name (str): GitHub repository in owner/repo format (e.g. "facebook/react").
        question (str): The question to ask about the repository.

    Returns:
        dict: Answer from DeepWiki about the repository.
    """
    try:
        response = httpx.post(
            "https://api.deepwiki.com/v1/chat/completions",
            headers={"Content-Type": "application/json"},
            json={
                "model": "deepwiki",
                "messages": [
                    {
                        "role": "user",
                        "content": f"@{repo_name} {question}",
                    }
                ],
            },
            timeout=30.0,
        )
        response.raise_for_status()
        data = response.json()
        answer = data.get("choices", [{}])[0].get("message", {}).get("content", "No answer available.")
        return {"status": "success", "repo": repo_name, "answer": answer}
    except Exception as e:
        return {"status": "error", "error_message": f"Failed to query DeepWiki: {str(e)}"}


SYSTEM_INSTRUCTION = f"""You are the Devin AI Customer Support Agent — a friendly, knowledgeable
assistant that helps users understand and get the most out of Devin, the AI software engineer
built by Cognition Labs.

## Your Role
- Answer questions about Devin AI: features, pricing, capabilities, limitations, integrations,
  best practices, and troubleshooting.
- Be helpful, concise, and accurate. Always base your answers on official Devin documentation.
- If you don't know something, say so honestly and suggest checking docs.devin.ai.
- When discussing pricing, always use the get_pricing_details tool for accurate numbers.
- When listing features or capabilities, use the get_feature_list tool.
- When asked about integrations, use the get_integration_list tool.
- For common questions, use the get_faq tool first.
- When users ask about a specific GitHub repository's documentation, use the DeepWiki tools
  to look it up (read_wiki_structure, read_wiki_contents, or ask_question).

## Core Knowledge

{knowledge.DEVIN_OVERVIEW}

### Strengths
{knowledge.DEVIN_STRENGTHS}

### Limitations
{knowledge.DEVIN_LIMITATIONS}

### Interface
{knowledge.DEVIN_INTERFACE}

### Best Practices
{knowledge.BEST_PRACTICES}

## Guidelines
- Format responses with clear structure using markdown when helpful.
- For pricing questions, always mention the ACU model and the three plans (Core, Teams, Enterprise).
- Proactively suggest best practices when relevant.
- If a user seems frustrated, be empathetic and offer actionable solutions.
- Always recommend docs.devin.ai for the latest and most detailed information.
- You can look up GitHub repository documentation using DeepWiki when asked about specific repos.
"""


root_agent = Agent(
    name="devin_support_agent",
    model="gemini-2.0-flash",
    description=(
        "Customer support agent that answers questions about Devin AI — "
        "the autonomous AI software engineer by Cognition Labs. "
        "Handles FAQ, pricing, features, integrations, and best practices."
    ),
    instruction=SYSTEM_INSTRUCTION,
    tools=[
        get_pricing_details,
        get_feature_list,
        get_integration_list,
        get_faq,
        deepwiki_ask,
    ],
)
