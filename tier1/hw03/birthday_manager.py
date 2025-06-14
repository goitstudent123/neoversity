import json
from datetime import date, datetime, timedelta
from typing import Optional


def get_upcoming_birthdays(
    users: list[dict],
    date_format: str = "%Y.%m.%d",
    today: Optional[date] = None,  # <-- правильний тип
) -> list[dict]:
    """
    Returns a list of users whose birthdays are within the next 7 days (including today).

    :param users: List of dictionaries containing user data with 'name' and 'birthday' keys
    :param date_format: Date format string (default: "%Y-%m-%d")
    :param today: Optional date to use as reference point (default: current date)
    :return: List of dictionaries with 'name' and 'congratulation_date' for upcoming birthdays
    :raises ValueError: If birthday value is not in valid date format
    """

    def adjust_weekend(current_date: date) -> date:
        if current_date.weekday() == 5:
            return current_date + timedelta(days=2)
        if current_date.weekday() == 6:
            return current_date + timedelta(days=1)
        return current_date

    today = today or datetime.today().date()
    end_date = today + timedelta(days=7)
    result = []

    for user in users:
        name = user["name"]
        birthday = datetime.strptime(user["birthday"], date_format).date()
        try:
            birthday_this_year = birthday.replace(year=today.year)
        except ValueError:
            birthday_this_year = date(today.year, 3, 1)  # move Feb 29 → Mar 1

        if birthday_this_year < today:
            birthday_this_year = birthday_this_year.replace(year=today.year + 1)

        if today <= birthday_this_year <= end_date:
            congratulation_date = adjust_weekend(birthday_this_year)

            result.append(
                {"name": name, "congratulation_date": congratulation_date.strftime("%Y.%m.%d")}
            )

    return result


if __name__ == "__main__":
    users = [
        {"name": "John Doe", "birthday": "1985.01.23"},
        {"name": "Jane Smith", "birthday": "1990.01.27"},
    ]
    upcoming_birthdays = get_upcoming_birthdays(users, today=date(2024, 1, 22))
    print("Список привітань на цьому тижні:", json.dumps(upcoming_birthdays, indent=4))
