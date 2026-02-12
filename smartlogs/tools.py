"""Tools for the SmartLogs agent."""

import re


def parse_log(log_entry: str) -> dict:
    """Parse a log entry and extract structured information.

    Handles both single-line log entries and multi-line stack traces.
    For multi-line input the first line is parsed for severity/message and
    remaining lines are collected into a ``stacktrace`` list.

    Args:
        log_entry: Raw log string, possibly containing newline-separated
            stack trace frames.

    Returns:
        Dictionary with parsed fields: severity, message, timestamp (if present),
        stacktrace (list of strings), and the raw log.
    """
    lines = log_entry.strip().splitlines()
    first_line = lines[0] if lines else ""

    severity_pattern = r"^(DEBUG|INFO|WARNING|WARN|ERROR|CRITICAL|FATAL)"
    match = re.match(severity_pattern, first_line.strip(), re.IGNORECASE)

    severity = match.group(1).upper() if match else "UNKNOWN"
    message = first_line.strip()

    if match:
        message = first_line[match.end():].strip().lstrip(":").strip()

    timestamp_pattern = r"\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}"
    ts_match = re.search(timestamp_pattern, first_line)
    timestamp = ts_match.group(0) if ts_match else None

    stacktrace: list[str] = [
        line.rstrip() for line in lines[1:] if line.strip()
    ]

    return {
        "severity": severity,
        "message": message,
        "timestamp": timestamp,
        "stacktrace": stacktrace,
        "raw": log_entry.strip(),
    }


def classify_severity(log_entry: str) -> str:
    """Classify the severity level of a log entry.

    Args:
        log_entry: Raw log string

    Returns:
        Severity level string: INFO, WARNING, ERROR, or CRITICAL
    """
    entry_upper = log_entry.upper()
    if "CRITICAL" in entry_upper or "FATAL" in entry_upper:
        return "CRITICAL"
    elif "ERROR" in entry_upper:
        return "ERROR"
    elif "WARN" in entry_upper:
        return "WARNING"
    return "INFO"


def format_analysis(analysis: dict) -> str:
    """Format an analysis result into human-readable text.

    Args:
        analysis: Dictionary with analysis results

    Returns:
        Formatted string for terminal display
    """
    lines = []
    lines.append(f"Log Analysis Report")
    lines.append("=" * 40)

    if "severity" in analysis:
        lines.append(f"Severity: {analysis['severity']}")
    if "error_type" in analysis:
        lines.append(f"Error Type: {analysis['error_type']}")
    if "root_cause" in analysis:
        lines.append(f"Root Cause: {analysis['root_cause']}")

    if "suggested_fixes" in analysis:
        lines.append("\nSuggested Fixes:")
        for i, fix in enumerate(analysis["suggested_fixes"], 1):
            lines.append(f"  {i}. {fix}")

    if "summary" in analysis:
        lines.append(f"\nSummary: {analysis['summary']}")

    return "\n".join(lines)
