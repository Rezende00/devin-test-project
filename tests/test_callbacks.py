"""Tests for conversation memory callbacks."""

from unittest.mock import MagicMock, patch

import pytest

from devin_support_agent.callbacks import (
    TOOL_TOPIC_MAP,
    inject_conversation_context,
    track_conversation_topic,
)


class _FakeState(dict):
    """Dict-like stand-in for ADK State used in tests."""


def _make_tool(name: str) -> MagicMock:
    tool = MagicMock()
    tool.name = name
    return tool


def _make_tool_context(state: dict | None = None) -> MagicMock:
    ctx = MagicMock()
    ctx.state = _FakeState(state or {})
    return ctx


def _make_callback_context(state: dict | None = None) -> MagicMock:
    ctx = MagicMock()
    ctx.state = _FakeState(state or {})
    return ctx


def _make_llm_request() -> MagicMock:
    req = MagicMock()
    req.append_instructions = MagicMock()
    return req


class TestTrackConversationTopic:
    def test_stores_topic_for_known_tool(self):
        tool = _make_tool("get_pricing_details")
        ctx = _make_tool_context()

        result = track_conversation_topic(tool, {}, ctx, {})

        assert result is None
        assert ctx.state["last_topic"] == "pricing and plans"
        assert ctx.state["last_tool"] == "get_pricing_details"

    def test_stores_topic_for_each_known_tool(self):
        for tool_name, expected_topic in TOOL_TOPIC_MAP.items():
            if tool_name == "deepwiki_ask":
                continue
            tool = _make_tool(tool_name)
            ctx = _make_tool_context()

            track_conversation_topic(tool, {}, ctx, {})

            assert ctx.state["last_topic"] == expected_topic

    def test_deepwiki_includes_repo_name(self):
        tool = _make_tool("deepwiki_ask")
        ctx = _make_tool_context()

        track_conversation_topic(
            tool, {"repo_name": "facebook/react"}, ctx, {}
        )

        assert ctx.state["last_topic"] == "DeepWiki lookup for facebook/react"
        assert ctx.state["last_tool"] == "deepwiki_ask"

    def test_deepwiki_without_repo_name_falls_back(self):
        tool = _make_tool("deepwiki_ask")
        ctx = _make_tool_context()

        track_conversation_topic(tool, {}, ctx, {})

        assert ctx.state["last_topic"] == TOOL_TOPIC_MAP["deepwiki_ask"]

    def test_unknown_tool_uses_tool_name(self):
        tool = _make_tool("some_new_tool")
        ctx = _make_tool_context()

        track_conversation_topic(tool, {}, ctx, {})

        assert ctx.state["last_topic"] == "some_new_tool"
        assert ctx.state["last_tool"] == "some_new_tool"


class TestInjectConversationContext:
    def test_no_injection_when_no_last_topic(self):
        ctx = _make_callback_context()
        req = _make_llm_request()

        result = inject_conversation_context(ctx, req)

        assert result is None
        req.append_instructions.assert_not_called()

    def test_injects_context_when_last_topic_exists(self):
        ctx = _make_callback_context({"last_topic": "pricing and plans"})
        req = _make_llm_request()

        result = inject_conversation_context(ctx, req)

        assert result is None
        req.append_instructions.assert_called_once()
        instructions = req.append_instructions.call_args[0][0]
        assert len(instructions) == 1
        assert "pricing and plans" in instructions[0]

    def test_injection_includes_follow_up_guidance(self):
        ctx = _make_callback_context({"last_topic": "integrations"})
        req = _make_llm_request()

        inject_conversation_context(ctx, req)

        instructions = req.append_instructions.call_args[0][0]
        assert "follow-up" in instructions[0].lower()


class TestAgentWiring:
    def test_agent_has_callbacks_registered(self):
        from devin_support_agent.agent import root_agent

        assert root_agent.before_model_callback is not None
        assert root_agent.after_tool_callback is not None

    def test_agent_instruction_contains_continuity_section(self):
        from devin_support_agent.agent import SYSTEM_INSTRUCTION

        assert "Conversation Continuity" in SYSTEM_INSTRUCTION

    def test_agent_loads_without_error(self):
        from devin_support_agent.agent import root_agent

        assert root_agent.name == "devin_support_agent"
        assert len(root_agent.tools) == 5
