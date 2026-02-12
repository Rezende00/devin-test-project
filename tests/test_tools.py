"""Tests for SmartLogs tools."""

from smartlogs.tools import parse_log, classify_severity, format_analysis


class TestParseLog:
    def test_parse_error_log(self):
        result = parse_log("ERROR: Connection refused on port 5432")
        assert result["severity"] == "ERROR"
        assert "Connection refused" in result["message"]
        assert result["timestamp"] is None

    def test_parse_warning_log(self):
        result = parse_log("WARNING: Disk usage above 90%")
        assert result["severity"] == "WARNING"
        assert "Disk usage" in result["message"]

    def test_parse_info_log(self):
        result = parse_log("INFO: Server started on port 8080")
        assert result["severity"] == "INFO"
        assert "Server started" in result["message"]

    def test_parse_log_with_timestamp(self):
        result = parse_log("2024-01-15T14:30:00 ERROR: Database timeout")
        assert result["timestamp"] == "2024-01-15T14:30:00"

    def test_parse_unknown_severity(self):
        result = parse_log("Something went wrong with the connection")
        assert result["severity"] == "UNKNOWN"

    def test_parse_multiline_stacktrace(self):
        """This test documents the known bug: parser only handles single-line logs."""
        multiline = "ERROR: NullPointerException\n  at com.app.Main.run(Main.java:42)\n  at com.app.Main.main(Main.java:10)"
        result = parse_log(multiline)
        assert result["severity"] == "ERROR"


class TestClassifySeverity:
    def test_critical(self):
        assert classify_severity("CRITICAL: System out of memory") == "CRITICAL"

    def test_fatal(self):
        assert classify_severity("FATAL: Kernel panic") == "CRITICAL"

    def test_error(self):
        assert classify_severity("ERROR: File not found") == "ERROR"

    def test_warning(self):
        assert classify_severity("WARN: Deprecated API used") == "WARNING"

    def test_info_default(self):
        assert classify_severity("Server started successfully") == "INFO"


class TestFormatAnalysis:
    def test_format_basic(self):
        analysis = {
            "severity": "ERROR",
            "error_type": "ConnectionError",
            "root_cause": "Database server is down",
            "suggested_fixes": ["Restart the database", "Check network connectivity"],
            "summary": "Database connection failed",
        }
        result = format_analysis(analysis)
        assert "ERROR" in result
        assert "ConnectionError" in result
        assert "Restart the database" in result
        assert "Database connection failed" in result

    def test_format_minimal(self):
        analysis = {"severity": "INFO"}
        result = format_analysis(analysis)
        assert "INFO" in result
