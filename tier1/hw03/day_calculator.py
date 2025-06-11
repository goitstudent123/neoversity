from datetime import datetime


def get_days_from_today(date: str, date_format: str = "%Y-%m-%d") -> int:
    """
    Calculates the number of days between a given date and the current date.

    :param date: String in valid date format
    :param date_format: Date format string (default: "%Y-%m-%d")
    :return: int (can be negative)
    :raises ValueError: If the date is not corresponded in valid date format
    """
    try:
        target_date = datetime.strptime(date, date_format).date()
        today = datetime.today().date()
        delta = today - target_date
        return delta.days
    except ValueError:
        raise ValueError(f"Incorrect date format, {date_format} expected")


if __name__ == "__main__":
    print(get_days_from_today("2021-10-09"))
