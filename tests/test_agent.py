import os
from unittest.mock import patch

from customer_support_agent.agent import create_agent


class TestAgentCreation:
    def test_default_agent_has_all_tools(self):
        agent = create_agent()
        tool_names = [t.__name__ for t in agent.tools]
        assert "get_order_status" in tool_names
        assert "refund_order" in tool_names
        assert "search_knowledge_base" in tool_names
        assert "analyze_sentiment" in tool_names

    @patch.dict(os.environ, {"ENABLE_RAG_TOOL": "false"})
    def test_rag_tool_disabled(self):
        import importlib

        import config

        importlib.reload(config)
        from config import ENABLE_RAG_TOOL

        assert ENABLE_RAG_TOOL is False

    @patch.dict(os.environ, {"ENABLE_SENTIMENT_ANALYSIS": "false"})
    def test_sentiment_disabled(self):
        import importlib

        import config

        importlib.reload(config)
        from config import ENABLE_SENTIMENT_ANALYSIS

        assert ENABLE_SENTIMENT_ANALYSIS is False

    def test_agent_has_name(self):
        agent = create_agent()
        assert agent.name == "customer_support_agent"

    def test_agent_has_instruction(self):
        agent = create_agent()
        assert "ShopEasy" in agent.instruction
