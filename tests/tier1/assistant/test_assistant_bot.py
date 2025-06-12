import pytest

from tier1.assistant.assistant_bot import (
    add_contact,
    change_contact,
    parse_input,
    show_all,
    show_phone,
)
from tier1.assistant.models import AddressBook, Record


@pytest.fixture
def john_address_book() -> AddressBook:
    return AddressBook({"John": Record("John", "1234567890")})


def test_parse_input_basic() -> None:
    assert parse_input("add John 123456") == ("add", ["John", "123456"])


def test_parse_input_strip_and_case() -> None:
    assert parse_input("  ADD  Alice 09876  ") == ("add", ["Alice", "09876"])


def test_parse_input_no_args() -> None:
    assert parse_input("all") == ("all", [])


def test_add_contact_success() -> None:
    contacts: AddressBook = AddressBook()
    result = add_contact(["John", "1234567890"], contacts)
    assert result == "Contact added."

    record = contacts.find("John")
    assert record is not None
    assert len(record.phones) == 1
    assert record.phones[0].value == "1234567890"


def test_add_contact_too_few_args() -> None:
    result = add_contact(["John"], AddressBook())
    assert result == "Invalid command format. Usage: add <name> <phone number>"


def test_add_contact_too_many_args() -> None:
    result = add_contact(["John", "12345", "extra"], AddressBook())
    assert result == "Invalid command format. Usage: add <name> <phone number>"


def test_change_contact_success(john_address_book: AddressBook) -> None:
    result = change_contact(["John", "1234567890", "0987654321"], john_address_book)
    assert result == "Contact phone updated."

    record = john_address_book.find("John")
    assert record is not None
    assert len(record.phones) == 1
    assert record.phones[0].value == "0987654321"


def test_change_contact_not_found() -> None:
    result = change_contact(["Jane", "54321", "54321"], AddressBook())
    assert result == "Contact not found."


def test_change_contact_too_few_args(john_address_book: AddressBook) -> None:
    result = change_contact(["John"], john_address_book)
    assert result == "Invalid command format. Usage: change <name> <old phone> <new phone>"


def test_change_contact_too_many_args() -> None:
    result = change_contact(["John", "12345", "12345", "extra"], AddressBook())
    assert result == "Invalid command format. Usage: change <name> <old phone> <new phone>"


def test_show_phone_success(john_address_book: AddressBook) -> None:
    assert show_phone(["John"], john_address_book) == "1234567890"


def test_show_phone_not_found() -> None:
    assert show_phone(["Bob"], AddressBook()) == "Contact not found."


def test_show_phone_too_few_args(john_address_book: AddressBook) -> None:
    assert show_phone([], john_address_book) == "Invalid command format. Usage: phone <name>"


def test_show_phone_too_many_args(john_address_book: AddressBook) -> None:
    assert (
        show_phone(["John", "extra"], john_address_book)
        == "Invalid command format. Usage: phone <name>"
    )


def test_show_all_with_contacts() -> None:
    contacts = AddressBook()
    contacts.add_record(Record("A", "0000000000"))
    contacts.add_record(Record("B", "1111111111"))
    output = show_all(contacts)
    lines = output.splitlines()
    assert "Contact name: A, phones: 0000000000" in lines
    assert "Contact name: B, phones: 1111111111" in lines


def test_show_all_no_contacts() -> None:
    assert show_all(AddressBook()) == "No contacts saved."
