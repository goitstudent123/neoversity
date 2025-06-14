from datetime import datetime, timedelta

from tier1.hw03.day_calculator import get_days_from_today


def test_today_standard_format() -> None:
    today = datetime.today().date()
    assert get_days_from_today(date=today.strftime("%Y-%m-%d")) == 0


def test_yesterday() -> None:
    today = datetime.today().date()
    assert get_days_from_today((today - timedelta(days=1)).strftime("%Y-%m-%d")) == 1


def test_tomorrow() -> None:
    today = datetime.today().date()
    assert get_days_from_today((today + timedelta(days=1)).strftime("%Y-%m-%d")) == -1


def test_different_format_dm_y() -> None:
    today = datetime.today().date()
    assert get_days_from_today(today.strftime("%d.%m.%Y"), "%d.%m.%Y") == 0


def test_different_format_md_y() -> None:
    today = datetime.today().date()
    assert get_days_from_today(today.strftime("%m/%d/%Y"), "%m/%d/%Y") == 0


def test_iso_format_with_time() -> None:
    iso_string = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    try:
        get_days_from_today(iso_string)
    except ValueError as e:
        assert "Incorrect date format" in str(e)
    else:
        assert False, "Expected ValueError due to wrong format"


def test_invalid_date() -> None:
    try:
        get_days_from_today("31-02-2020", "%d-%m-%Y")
    except ValueError as e:
        assert "Incorrect date format" in str(e)
    else:
        assert False, "Expected ValueError for invalid date"
