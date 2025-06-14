from unittest.mock import MagicMock, mock_open, patch

import pytest

from tier1.assistant.assistant_bot import (
    ADDRESSBOOK_FILE_NAME,
    CONTACT_NOT_FOUND,
    add_contact,
    change_contact,
    main,
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
    result, save_flag = add_contact(["John", "1234567890"], contacts)
    assert result == "Contact added."
    assert save_flag is True

    record = contacts.find("John")
    assert record is not None
    assert len(record.phones) == 1
    assert record.phones[0].value == "1234567890"


def test_add_contact_too_few_args() -> None:
    result, save_flag = add_contact(["John"], AddressBook())
    assert result == "Invalid command format. Usage: add <name> <phone number>"
    assert save_flag is False


def test_add_contact_too_many_args() -> None:
    result, save_flag = add_contact(["John", "12345", "extra"], AddressBook())
    assert result == "Invalid command format. Usage: add <name> <phone number>"
    assert save_flag is False


def test_change_contact_success(john_address_book: AddressBook) -> None:
    result, save_flag = change_contact(["John", "1234567890", "0987654321"], john_address_book)
    assert result == "Contact phone updated."
    assert save_flag is True

    record = john_address_book.find("John")
    assert record is not None
    assert len(record.phones) == 1
    assert record.phones[0].value == "0987654321"


def test_change_contact_not_found() -> None:
    result, save_flag = change_contact(["Jane", "54321", "54321"], AddressBook())
    assert result == CONTACT_NOT_FOUND
    assert save_flag is False


def test_change_contact_too_few_args(john_address_book: AddressBook) -> None:
    result, save_flag = change_contact(["John"], john_address_book)
    assert result == "Invalid command format. Usage: change <name> <old phone> <new phone>"
    assert save_flag is False


def test_change_contact_too_many_args() -> None:
    result, save_flag = change_contact(["John", "12345", "12345", "extra"], AddressBook())
    assert result == "Invalid command format. Usage: change <name> <old phone> <new phone>"
    assert save_flag is False


def test_show_phone_success(john_address_book: AddressBook) -> None:
    assert show_phone(["John"], john_address_book) == ("1234567890", False)


def test_show_phone_not_found() -> None:
    assert show_phone(["Bob"], AddressBook()) == (CONTACT_NOT_FOUND, False)


def test_show_phone_too_few_args(john_address_book: AddressBook) -> None:
    assert show_phone([], john_address_book) == (
        "Invalid command format. Usage: phone <name>",
        False,
    )


def test_show_phone_too_many_args(john_address_book: AddressBook) -> None:
    assert show_phone(["John", "extra"], john_address_book) == (
        "Invalid command format. Usage: phone <name>",
        False,
    )


def test_show_all_with_contacts() -> None:
    contacts = AddressBook()
    contacts.add_record(Record("A", "0000000000"))
    contacts.add_record(Record("B", "1111111111"))
    output, save_flag = show_all(contacts)
    assert save_flag is False
    lines = output.splitlines()
    assert "Contact name: A, phones: 0000000000" in lines
    assert "Contact name: B, phones: 1111111111" in lines


def test_show_all_no_contacts() -> None:
    assert show_all(AddressBook()) == ("No contacts saved.", False)


def test_main_add_change_exit_flow() -> None:
    mock_inputs = iter(
        [
            "add Alice 1111111111",  # Add a contact
            "change Alice 1111111111 2222222222",  # Change phone
            "exit",
        ]
    )

    dummy_book = AddressBook()

    mock_open_file = mock_open()
    mock_pickle_dump = MagicMock()
    mock_pickle_load = MagicMock(return_value=dummy_book)

    with patch("builtins.input", lambda _: next(mock_inputs)), patch(
        "builtins.open", mock_open_file
    ), patch("pickle.dump", mock_pickle_dump), patch("pickle.load", mock_pickle_load):
        main()

        mock_open_file.assert_any_call(ADDRESSBOOK_FILE_NAME, "rb")
        assert mock_pickle_load.call_count == 1

        assert mock_pickle_dump.call_count == 2

        assert "Alice" in dummy_book.data
        record = dummy_book.find("Alice")
        assert record is not None
        assert record.phones[0].value == "2222222222"
