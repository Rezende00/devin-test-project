"""Devin AI Customer Support Agent — tool functions."""

import httpx

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
