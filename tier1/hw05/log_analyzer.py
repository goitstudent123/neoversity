import sys
from collections import defaultdict
from typing import Any, Dict, List


def parse_log_line(line: str) -> dict:
    parts = line.strip().split(" ", 3)
    if len(parts) < 4:
        return {}
    date, time, level, message = parts
    return {"date": date, "time": time, "level": level.upper(), "message": message}


def load_logs(file_path: str) -> List[dict]:
    logs = []
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            logs = [parsed for line in file if (parsed := parse_log_line(line))]
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)
    return logs


def filter_logs_by_level(logs: List[dict], level: str) -> List[dict]:
    return list(filter(lambda log: log["level"] == level.upper(), logs))


def count_logs_by_level(logs: List[dict]) -> Dict[str, int]:
    counts: defaultdict[Any, int] = defaultdict(int)
    for log in logs:
        counts[log["level"]] += 1
    return dict(counts)


def display_log_counts(counts: Dict[str, int]) -> None:
    print("\nРівень логування | Кількість")
    print("-----------------|----------")
    for level in sorted(counts.keys()):
        print(f"{level:<17} | {counts[level]}")


def display_filtered_logs(logs: List[dict], level: str) -> None:
    print(f"\nДеталі логів для рівня '{level.upper()}':")
    for log in logs:
        print(f"{log['date']} {log['time']} - {log['message']}")


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python log_analyzer.py <path_to_log_file> [level]")
        sys.exit(1)

    file_path = sys.argv[1]
    level_filter = sys.argv[2] if len(sys.argv) > 2 else None

    logs = load_logs(file_path)
    counts = count_logs_by_level(logs)
    display_log_counts(counts)

    if level_filter:
        filtered = filter_logs_by_level(logs, level_filter)
        display_filtered_logs(filtered, level_filter)


if __name__ == "__main__":
    main()
