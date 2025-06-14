import pickle
from typing import Any, Callable, Tuple, TypeVar, cast

from tier1.assistant.models import AddressBook, Record

CONTACT_NOT_FOUND = "Contact not found."
ADDRESSBOOK_FILE_NAME = "addressbook.pkl"

F = TypeVar("F", bound=Callable[..., Any])


def input_error(error_hint: str = "Enter the argument for the command") -> Callable[[F], F]:
    def decorator(func: F) -> F:
        def inner(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except KeyError:
                return CONTACT_NOT_FOUND, False
            except ValueError as e:
                return f"{e}, {error_hint}", False
            except IndexError:
                return error_hint, False

        return inner  # type: ignore

    return decorator


def parse_input(user_input: str) -> tuple[str, list[str]]:
    cmd, *args = user_input.strip().split()
    return cmd.lower(), args


@input_error("Invalid command format. Usage: add <name> <phone number>")
def add_contact(args: list[str], book: AddressBook) -> Tuple[str, bool]:
    if len(args) != 2:
        raise IndexError
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message, True


@input_error("Invalid command format. Usage: change <name> <old phone> <new phone>")
def change_contact(args: list[str], book: AddressBook) -> Tuple[str, bool]:
    if len(args) != 3:
        raise IndexError
    name, old_phone, new_phone = args
    record = book.find(name)
    if record is None:
        return CONTACT_NOT_FOUND, False
    if not record.edit_phone(old_phone, new_phone):
        return "Old phone number not found.", False
    return "Contact phone updated.", True


@input_error("Invalid command format. Usage: phone <name>")
def show_phone(args: list[str], book: AddressBook) -> Tuple[str, bool]:
    if len(args) != 1:
        raise IndexError
    name = args[0]
    record = book.find(name)
    if record is None:
        return CONTACT_NOT_FOUND, False
    return "; ".join(p.value for p in record.phones), False


def show_all(book: AddressBook) -> Tuple[str, bool]:
    if not book.data:
        return "No contacts saved.", False
    return "\n".join(str(record) for record in book.data.values()), False


@input_error("Invalid command format. Usage: add-birthday <name> <DD.MM.YYYY>")
def add_birthday(args: list[str], book: AddressBook) -> Tuple[str, bool]:
    if len(args) != 2:
        raise IndexError
    name, bday = args
    record = book.find(name)
    if record is None:
        return CONTACT_NOT_FOUND, False
    record.add_birthday(bday)
    return "Birthday added.", True


@input_error("Invalid command format. Usage: show-birthday <name>")
def show_birthday(args: list[str], book: AddressBook) -> Tuple[str, bool]:
    if len(args) != 1:
        raise IndexError
    name = args[0]
    record = book.find(name)
    if record is None or record.birthday is None:
        return "Birthday not found.", False
    return record.birthday.value.strftime("%d.%m.%Y"), False


@input_error("birthdays command doesn't take any arguments")
def birthdays(args: list[str], book: AddressBook) -> Tuple[str, bool]:
    result = book.get_upcoming_birthdays()
    if not result:
        return "No upcoming birthdays.", False
    return "\n".join(f"{entry['name']}: {entry['congratulation_date']}" for entry in result), False


def save_data(book: AddressBook, filename: str = ADDRESSBOOK_FILE_NAME) -> None:
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename: str = ADDRESSBOOK_FILE_NAME) -> AddressBook:
    try:
        with open(filename, "rb") as f:
            data = pickle.load(f)
            return cast(AddressBook, data)
    except FileNotFoundError:
        return AddressBook()


def handle_command(command: str, args: list[str], book: AddressBook) -> Tuple[str, bool]:
    match command:
        case "add":
            return add_contact(args, book)
        case "change":
            return change_contact(args, book)
        case "phone":
            return show_phone(args, book)
        case "all":
            return show_all(book)
        case "hello":
            return "How can I help you?", False
        case "add-birthday":
            return add_birthday(args, book)
        case "show-birthday":
            return show_birthday(args, book)
        case "birthdays":
            return birthdays(args, book)
        case _:
            return "Invalid command.", False


def main() -> None:
    book = load_data()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)
        if command in ["close", "exit"]:
            print("Good bye!")
            break
        else:
            cmd_output, need_save = handle_command(command, args, book)

        if need_save:
            save_data(book)
        print(cmd_output)


if __name__ == "__main__":
    main()
