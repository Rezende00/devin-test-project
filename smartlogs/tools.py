"""Tools for the SmartLogs agent."""

import re


def parse_log(log_entry: str) -> dict:
    """Parse a log entry and extract structured information.

    Args:
        log_entry: Raw log string (e.g. "ERROR: Connection refused on port 5432")

    Returns:
        Dictionary with parsed fields: severity, message, timestamp (if present),
        source (if present), and the raw log.
    """
    severity_pattern = r"^(DEBUG|INFO|WARNING|WARN|ERROR|CRITICAL|FATAL)"
    match = re.match(severity_pattern, log_entry.strip(), re.IGNORECASE)

    severity = match.group(1).upper() if match else "UNKNOWN"
    message = log_entry.strip()

    if match:
        message = log_entry[match.end():].strip().lstrip(":").strip()

    timestamp_pattern = r"\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}"
    ts_match = re.search(timestamp_pattern, log_entry)
    timestamp = ts_match.group(0) if ts_match else None

    return {
        "severity": severity,
        "message": message,
        "timestamp": timestamp,
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
