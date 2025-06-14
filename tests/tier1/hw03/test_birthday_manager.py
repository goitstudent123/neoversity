from datetime import datetime

from tier1.hw03.birthday_manager import get_upcoming_birthdays


def test_birthdays_basic() -> None:
    users = [
        {"name": "John Doe", "birthday": "1985.01.23"},
        {"name": "Jane Smith", "birthday": "1990.01.27"},
        {"name": "Bob Johnson", "birthday": "1988.01.28"},
    ]

    test_date = datetime.strptime("2024.01.22", "%Y.%m.%d").date()
    result = get_upcoming_birthdays(users, date_format="%Y.%m.%d", today=test_date)
    expected = [
        {"name": "John Doe", "congratulation_date": "2024.01.23"},
        {"name": "Jane Smith", "congratulation_date": "2024.01.29"},  # 27 is Saturday
        {"name": "Bob Johnson", "congratulation_date": "2024.01.29"},
    ]
    assert result == expected


def test_weekend_shift() -> None:
    users = [{"name": "Weekend Person", "birthday": "1992.01.28"}]
    test_date = datetime.strptime("2024.01.22", "%Y.%m.%d").date()

    result = get_upcoming_birthdays(users, date_format="%Y.%m.%d", today=test_date)
    expected = [{"name": "Weekend Person", "congratulation_date": "2024.01.29"}]
    assert result == expected
