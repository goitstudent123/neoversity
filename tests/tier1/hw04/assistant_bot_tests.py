from tier1.hw04.assistant_bot import add_contact, change_contact, parse_input, show_all, show_phone


def test_parse_input_basic() -> None:
    assert parse_input("add John 123456") == ("add", ["John", "123456"])


def test_parse_input_strip_and_case() -> None:
    assert parse_input("  ADD  Alice 09876  ") == ("add", ["Alice", "09876"])


def test_parse_input_no_args() -> None:
    assert parse_input("all") == ("all", [])


def test_add_contact_success() -> None:
    contacts: dict[str, str] = {}
    result = add_contact(["John", "12345"], contacts)
    assert result == "Contact added."
    assert contacts == {"John": "12345"}


def test_add_contact_too_few_args() -> None:
    result = add_contact(["John"], {})
    assert result == "Invalid command format. Usage: add <name> <phone number>"


def test_add_contact_too_many_args() -> None:
    result = add_contact(["John", "12345", "extra"], {})
    assert result == "Invalid command format. Usage: add <name> <phone number>"


def test_change_contact_success() -> None:
    contacts = {"John": "12345"}
    result = change_contact(["John", "54321"], contacts)
    assert result == "Contact updated."
    assert contacts == {"John": "54321"}


def test_change_contact_not_found() -> None:
    result = change_contact(["Jane", "54321"], {})
    assert result == "Contact not found."


def test_change_contact_too_few_args() -> None:
    result = change_contact(["John"], {"John": "12345"})
    assert result == "Invalid command format. Usage: change <name> <phone number>"


def test_change_contact_too_many_args() -> None:
    result = change_contact(["John", "12345", "extra"], {"John": "12345"})
    assert result == "Invalid command format. Usage: change <name> <phone number>"


def test_show_phone_success() -> None:
    contacts = {"Alice": "11111"}
    assert show_phone(["Alice"], contacts) == "11111"


def test_show_phone_not_found() -> None:
    assert show_phone(["Bob"], {}) == "Contact not found."


def test_show_phone_too_few_args() -> None:
    assert show_phone([], {"Bob": "22222"}) == "Invalid command format. Usage: phone <name>"


def test_show_phone_too_many_args() -> None:
    assert (
        show_phone(["Bob", "extra"], {"Bob": "22222"})
        == "Invalid command format. Usage: phone <name>"
    )


def test_show_all_with_contacts() -> None:
    contacts = {"A": "1", "B": "2"}
    output = show_all(contacts)
    lines = output.splitlines()
    assert "A: 1" in lines
    assert "B: 2" in lines


def test_show_all_no_contacts() -> None:
    assert show_all({}) == "No contacts saved."
