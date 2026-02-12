"""Tests for CLI retry logic around agent API calls."""

from unittest.mock import patch, MagicMock

import pytest
from click import ClickException
from google.api_core.exceptions import (
    TooManyRequests,
    InternalServerError,
    BadGateway,
    ServiceUnavailable,
    Unauthorized,
    Forbidden,
)

from smartlogs.cli import run_agent


def _make_final_event(text: str) -> MagicMock:
    part = MagicMock()
    part.text = text
    event = MagicMock()
    event.is_final_response.return_value = True
    event.content.parts = [part]
    return event


AGENT_PATCHES = [
    patch("smartlogs.cli.create_agent"),
    patch("smartlogs.cli.InMemorySessionService"),
]


class TestRetryOnTransientErrors:
    @pytest.mark.parametrize(
        "exception_cls",
        [TooManyRequests, InternalServerError, BadGateway, ServiceUnavailable],
    )
    @patch("smartlogs.cli.time.sleep")
    @patch("smartlogs.cli.Runner")
    def test_retries_then_succeeds(self, mock_runner_cls, mock_sleep, exception_cls):
        with AGENT_PATCHES[0], AGENT_PATCHES[1]:
            runner_instance = MagicMock()
            mock_runner_cls.return_value = runner_instance

            success_event = _make_final_event("analysis result")
            runner_instance.run.side_effect = [
                exception_cls("transient"),
                [success_event],
            ]

            result = run_agent("ERROR: something")

            assert result == "analysis result"
            assert runner_instance.run.call_count == 2
            mock_sleep.assert_called_once_with(1)

    @pytest.mark.parametrize(
        "exception_cls",
        [TooManyRequests, InternalServerError, BadGateway, ServiceUnavailable],
    )
    @patch("smartlogs.cli.time.sleep")
    @patch("smartlogs.cli.Runner")
    def test_exhausts_retries(self, mock_runner_cls, mock_sleep, exception_cls):
        with AGENT_PATCHES[0], AGENT_PATCHES[1]:
            runner_instance = MagicMock()
            mock_runner_cls.return_value = runner_instance

            runner_instance.run.side_effect = exception_cls("transient")

            with pytest.raises(ClickException, match="API call failed after 3 attempts"):
                run_agent("ERROR: something")

            assert runner_instance.run.call_count == 3
            assert mock_sleep.call_count == 2

    @patch("smartlogs.cli.time.sleep")
    @patch("smartlogs.cli.Runner")
    def test_exponential_backoff_timing(self, mock_runner_cls, mock_sleep):
        with AGENT_PATCHES[0], AGENT_PATCHES[1]:
            runner_instance = MagicMock()
            mock_runner_cls.return_value = runner_instance

            runner_instance.run.side_effect = ServiceUnavailable("transient")

            with pytest.raises(ClickException):
                run_agent("ERROR: something")

            sleep_args = [call.args[0] for call in mock_sleep.call_args_list]
            assert sleep_args == [1, 2]


class TestNoRetryOnAuthErrors:
    @pytest.mark.parametrize("exception_cls", [Unauthorized, Forbidden])
    @patch("smartlogs.cli.time.sleep")
    @patch("smartlogs.cli.Runner")
    def test_auth_errors_not_retried(self, mock_runner_cls, mock_sleep, exception_cls):
        with AGENT_PATCHES[0], AGENT_PATCHES[1]:
            runner_instance = MagicMock()
            mock_runner_cls.return_value = runner_instance

            runner_instance.run.side_effect = exception_cls("denied")

            with pytest.raises(exception_cls):
                run_agent("ERROR: something")

            assert runner_instance.run.call_count == 1
            mock_sleep.assert_not_called()


class TestMaxRetriesConfig:
    @patch("smartlogs.cli.time.sleep")
    @patch("smartlogs.cli.Runner")
    @patch("smartlogs.cli.get_max_retries", return_value=5)
    def test_custom_max_retries(self, mock_config, mock_runner_cls, mock_sleep):
        with AGENT_PATCHES[0], AGENT_PATCHES[1]:
            runner_instance = MagicMock()
            mock_runner_cls.return_value = runner_instance

            runner_instance.run.side_effect = ServiceUnavailable("transient")

            with pytest.raises(ClickException, match="API call failed after 5 attempts"):
                run_agent("ERROR: something")

            assert runner_instance.run.call_count == 5

    @patch("smartlogs.cli.time.sleep")
    @patch("smartlogs.cli.Runner")
    @patch("smartlogs.cli.get_max_retries", return_value=1)
    def test_single_retry_no_sleep(self, mock_config, mock_runner_cls, mock_sleep):
        with AGENT_PATCHES[0], AGENT_PATCHES[1]:
            runner_instance = MagicMock()
            mock_runner_cls.return_value = runner_instance

            runner_instance.run.side_effect = ServiceUnavailable("transient")

            with pytest.raises(ClickException):
                run_agent("ERROR: something")

            assert runner_instance.run.call_count == 1
            mock_sleep.assert_not_called()


class TestIterationFailure:
    @patch("smartlogs.cli.time.sleep")
    @patch("smartlogs.cli.Runner")
    def test_error_during_iteration(self, mock_runner_cls, mock_sleep):
        with AGENT_PATCHES[0], AGENT_PATCHES[1]:
            runner_instance = MagicMock()
            mock_runner_cls.return_value = runner_instance

            def failing_iterator(*args, **kwargs):
                yield _make_final_event("")
                raise ServiceUnavailable("mid-stream")

            success_event = _make_final_event("recovered")
            runner_instance.run.side_effect = [
                failing_iterator(),
                [success_event],
            ]

            result = run_agent("ERROR: something")

            assert result == "recovered"
            assert runner_instance.run.call_count == 2


class TestGetMaxRetries:
    def test_default_value(self):
        from smartlogs.config import get_max_retries

        with patch.dict("os.environ", {}, clear=False):
            with patch.dict("os.environ", {"SMARTLOGS_MAX_RETRIES": "3"}):
                assert get_max_retries() == 3

    def test_custom_value(self):
        from smartlogs.config import get_max_retries

        with patch.dict("os.environ", {"SMARTLOGS_MAX_RETRIES": "5"}):
            assert get_max_retries() == 5

    def test_invalid_value_returns_default(self):
        from smartlogs.config import get_max_retries

        with patch.dict("os.environ", {"SMARTLOGS_MAX_RETRIES": "abc"}):
            assert get_max_retries() == 3

    def test_negative_value_returns_zero(self):
        from smartlogs.config import get_max_retries

        with patch.dict("os.environ", {"SMARTLOGS_MAX_RETRIES": "-1"}):
            assert get_max_retries() == 0
