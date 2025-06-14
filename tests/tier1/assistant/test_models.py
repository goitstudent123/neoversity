from datetime import date

import pytest

from tier1.assistant.models import AddressBook, Phone, Record


@pytest.mark.parametrize(
    "bad_phone",
    [
        "123456789",  # 9 digits
        "12345678901",  # 11 digits
        "abcdefghij",  # not digits
        "12345abcde",  # mixed
        "",  # empty string
    ],
)
def test_invalid_phone_raises_value_error(bad_phone: str) -> None:
    with pytest.raises(ValueError, match="Phone number must be exactly 10 digits"):
        Phone(bad_phone)


def test_valid_phone_10_digits() -> None:
    phone = Phone("1234567890")
    assert phone.value == "1234567890"


def test_add_record_and_find() -> None:
    book = AddressBook()
    record = Record("Alice")
    record.add_phone("1234567890")
    book.add_record(record)

    found = book.find("Alice")
    assert found is not None
    assert found.name.value == "Alice"
    assert found.phones[0].value == "1234567890"


def test_edit_phone_success() -> None:
    record = Record("Bob")
    record.add_phone("1111111111")
    record.add_phone("2222222222")

    assert record.edit_phone("1111111111", "9999999999") is True
    assert any(p.value == "9999999999" for p in record.phones)


def test_edit_phone_not_found() -> None:
    record = Record("Charlie")
    record.add_phone("3333333333")

    assert record.edit_phone("0000000000", "4444444444") is False


def test_remove_phone_success() -> None:
    record = Record("Daisy")
    record.add_phone("1231231234")
    assert record.remove_phone("1231231234") is True
    assert len(record.phones) == 0


def test_remove_phone_not_found() -> None:
    record = Record("Eve")
    record.add_phone("7777777777")
    assert record.remove_phone("0000000000") is False
    assert len(record.phones) == 1


def test_find_phone_success() -> None:
    record = Record("Frank")
    record.add_phone("8888888888")
    phone = record.find_phone("8888888888")
    assert phone is not None
    assert isinstance(phone, Phone)


def test_find_phone_not_found() -> None:
    record = Record("Grace")
    record.add_phone("9999999999")
    assert record.find_phone("0000000000") is None


def test_delete_record_from_book() -> None:
    book = AddressBook()
    record = Record("Helen")
    book.add_record(record)
    assert book.delete("Helen") is True
    assert book.find("Helen") is None


def test_delete_non_existing_record() -> None:
    book = AddressBook()
    assert book.delete("NonExistent") is False


def test_get_upcoming_birthdays() -> None:
    ab = AddressBook()

    john = Record("John")
    john.add_phone("1234567890")
    john.add_birthday("15.06.2000")

    jane = Record("Jane")
    jane.add_phone("0987654321")
    jane.add_birthday("18.06.1995")

    alex = Record("Alex")
    alex.add_phone("1112223333")
    alex.add_birthday("30.06.1999")

    ab.add_record(john)
    ab.add_record(jane)
    ab.add_record(alex)

    today = date(2025, 6, 12)
    upcoming = ab.get_upcoming_birthdays(today=today)

    assert len(upcoming) == 2
    assert {"name": "John", "congratulation_date": "16.06.2025"} in upcoming
    assert {"name": "Jane", "congratulation_date": "18.06.2025"} in upcoming
    assert all("Alex" not in entry["name"] for entry in upcoming)
