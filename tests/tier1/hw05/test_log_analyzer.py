from tier1.hw05.log_analyzer import count_logs_by_level, filter_logs_by_level, parse_log_line


def test_parse_log_line_valid() -> None:
    line = "2024-01-22 08:30:01 INFO User logged in successfully."
    parsed = parse_log_line(line)
    assert parsed == {
        "date": "2024-01-22",
        "time": "08:30:01",
        "level": "INFO",
        "message": "User logged in successfully.",
    }


def test_parse_log_line_invalid() -> None:
    line = "invalid log line"
    parsed = parse_log_line(line)
    assert parsed == {}, f"Expected empty dict, got {parsed}"


def test_count_logs_by_level() -> None:
    logs = [
        {"level": "INFO"},
        {"level": "DEBUG"},
        {"level": "INFO"},
        {"level": "ERROR"},
        {"level": "DEBUG"},
    ]
    counts = count_logs_by_level(logs)
    assert counts == {"INFO": 2, "DEBUG": 2, "ERROR": 1}, f"Unexpected counts: {counts}"


def test_filter_logs_by_level_case_insensitive() -> None:
    logs = [
        {"level": "INFO", "message": "message 1"},
        {"level": "DEBUG", "message": "message 2"},
        {"level": "INFO", "message": "message 3"},
        {"level": "ERROR", "message": "message 4"},
    ]
    filtered = filter_logs_by_level(logs, "info")
    assert len(filtered) == 2
    assert all(log["level"] == "INFO" for log in filtered)
