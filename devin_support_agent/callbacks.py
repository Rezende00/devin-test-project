"""Callbacks for conversation memory and session state tracking."""

from typing import Optional

from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse
from google.adk.tools.base_tool import BaseTool
from google.adk.tools.tool_context import ToolContext

TOOL_TOPIC_MAP: dict[str, str] = {
    "get_pricing_details": "pricing and plans",
    "get_feature_list": "features and capabilities",
    "get_integration_list": "integrations",
    "get_faq": "frequently asked questions",
    "deepwiki_ask": "GitHub repository documentation via DeepWiki",
}


def track_conversation_topic(
    tool: BaseTool,
    args: dict[str, object],
    tool_context: ToolContext,
    tool_response: dict,
) -> Optional[dict]:
    """after_tool_callback: persist the last discussed topic in session state."""
    topic = TOOL_TOPIC_MAP.get(tool.name, tool.name)

    if tool.name == "deepwiki_ask" and "repo_name" in args:
        topic = f"DeepWiki lookup for {args['repo_name']}"

    tool_context.state["last_topic"] = topic
    tool_context.state["last_tool"] = tool.name

    return None


def inject_conversation_context(
    callback_context: CallbackContext,
    llm_request: LlmRequest,
) -> Optional[LlmResponse]:
    """before_model_callback: inject last-topic context into the LLM request."""
    last_topic = callback_context.state.get("last_topic")
    if not last_topic:
        return None

    context_hint = (
        f"[Conversation context] The user was most recently discussing: {last_topic}. "
        "If the user's new message is a follow-up (e.g. 'tell me more', "
        "'what about the Teams plan', 'how much does that cost'), "
        "use this context to resolve the reference. "
        "If the message is clearly a new, unrelated question, ignore this context."
    )

    llm_request.append_instructions([context_hint])

    return None
