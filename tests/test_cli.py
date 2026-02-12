"""Tests for SmartLogs CLI logging integration."""

import logging
from unittest.mock import patch

import pytest
from click.testing import CliRunner

from smartlogs.cli import main, setup_logging, LOG_FORMAT


@pytest.fixture(autouse=True)
def _reset_root_logger():
    """Reset root logger state between tests."""
    root = logging.getLogger()
    original_level = root.level
    original_handlers = root.handlers[:]
    yield
    root.setLevel(original_level)
    root.handlers = original_handlers


class TestSetupLogging:
    def test_default_level_is_info(self):
        setup_logging(verbose=False)
        root = logging.getLogger()
        assert root.level == logging.INFO

    def test_verbose_sets_debug(self):
        setup_logging(verbose=True)
        root = logging.getLogger()
        assert root.level == logging.DEBUG

    def test_log_format_contains_expected_fields(self):
        setup_logging(verbose=False)
        root = logging.getLogger()
        handler = root.handlers[-1]
        fmt = handler.formatter._fmt
        assert "%(asctime)s" in fmt
        assert "%(levelname)s" in fmt
        assert "%(name)s" in fmt


class TestCLIVerboseFlag:
    def test_verbose_flag_accepted(self):
        runner = CliRunner()
        result = runner.invoke(main, ["--verbose", "--help"])
        assert result.exit_code == 0

    def test_short_verbose_flag_accepted(self):
        runner = CliRunner()
        result = runner.invoke(main, ["-v", "--help"])
        assert result.exit_code == 0


class TestAnalyzeCommand:
    @patch("smartlogs.cli.run_agent", return_value="Mocked analysis result")
    def test_analyze_outputs_result_via_echo(self, mock_agent):
        runner = CliRunner()
        result = runner.invoke(main, ["analyze", "ERROR: test"])
        assert "Mocked analysis result" in result.output
        mock_agent.assert_called_once_with("ERROR: test")

    @patch("smartlogs.cli.run_agent", return_value="Mocked analysis result")
    def test_analyze_logs_info_message(self, mock_agent, caplog):
        runner = CliRunner()
        with caplog.at_level(logging.INFO, logger="smartlogs.cli"):
            runner.invoke(main, ["analyze", "ERROR: test"])
        assert any("Analyzing log entry" in r.message for r in caplog.records)

    @patch("smartlogs.cli.run_agent", return_value="Mocked analysis result")
    def test_analyze_verbose_enables_debug(self, mock_agent, caplog):
        runner = CliRunner()
        with caplog.at_level(logging.DEBUG, logger="smartlogs.cli"):
            runner.invoke(main, ["-v", "analyze", "ERROR: test"])
        log_names = [r.name for r in caplog.records]
        assert any(name.startswith("smartlogs") for name in log_names)


class TestAnalyzeFileCommand:
    @patch("smartlogs.cli.run_agent", return_value="Mocked result")
    def test_analyze_file_outputs_results(self, mock_agent, tmp_path):
        log_file = tmp_path / "test.log"
        log_file.write_text("ERROR: line1\nWARN: line2\n")
        runner = CliRunner()
        result = runner.invoke(main, ["analyze-file", str(log_file)])
        assert result.output.count("Mocked result") == 2

    @patch("smartlogs.cli.run_agent", return_value="Mocked result")
    def test_analyze_file_logs_entry_count(self, mock_agent, tmp_path, caplog):
        log_file = tmp_path / "test.log"
        log_file.write_text("ERROR: line1\nWARN: line2\n")
        runner = CliRunner()
        with caplog.at_level(logging.INFO, logger="smartlogs.cli"):
            runner.invoke(main, ["analyze-file", str(log_file)])
        assert any("Found 2 log entries" in r.message for r in caplog.records)


class TestToolsLogging:
    def test_parse_log_emits_debug(self, caplog):
        from smartlogs.tools import parse_log

        with caplog.at_level(logging.DEBUG, logger="smartlogs.tools"):
            parse_log("ERROR: something broke")
        assert any("Parsed log entry" in r.message for r in caplog.records)

    def test_classify_severity_emits_debug(self, caplog):
        from smartlogs.tools import classify_severity

        with caplog.at_level(logging.DEBUG, logger="smartlogs.tools"):
            classify_severity("ERROR: something broke")
        assert any("Classified severity" in r.message for r in caplog.records)
