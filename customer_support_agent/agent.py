from google.adk.agents.llm_agent import Agent

from config import (
    ENABLE_RAG_TOOL,
    ENABLE_SENTIMENT_ANALYSIS,
    USE_GEMINI_1_5_PRO,
    USE_STREAMING_RESPONSE,
)
from customer_support_agent.prompts import (
    RAG_TOOL_INSTRUCTION,
    SENTIMENT_INSTRUCTION,
    SYSTEM_INSTRUCTION,
)
from customer_support_agent.tools import (
    analyze_sentiment,
    get_order_status,
    refund_order,
    search_knowledge_base,
)


def create_agent() -> Agent:
    """Creates and configures the customer support agent based on feature flags."""
    tools = [get_order_status, refund_order]

    instruction = SYSTEM_INSTRUCTION

    if ENABLE_RAG_TOOL:
        tools.append(search_knowledge_base)
        instruction += RAG_TOOL_INSTRUCTION
    else:
        pass

    if ENABLE_SENTIMENT_ANALYSIS:
        tools.append(analyze_sentiment)
        instruction += SENTIMENT_INSTRUCTION
    else:
        pass

    if USE_GEMINI_1_5_PRO:
        model = "gemini-1.5-pro"
    else:
        model = "gemini-2.0-flash"

    if USE_STREAMING_RESPONSE:
        description = "ShopEasy Customer Support Agent (Streaming Mode)"
    else:
        description = "ShopEasy Customer Support Agent"

    agent = Agent(
        model=model,
        name="customer_support_agent",
        description=description,
        instruction=instruction,
        tools=tools,
    )

    return agent
