from typing import Any, Callable, TypeVar

from tier1.assistant.models import AddressBook, Record

F = TypeVar("F", bound=Callable[..., Any])


def input_error(error_hint: str = "Enter the argument for the command") -> Callable[[F], F]:
    def decorator(func: F) -> F:
        def inner(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except KeyError:
                return "Contact not found."
            except ValueError as e:
                return f"{e}, {error_hint}"
            except IndexError:
                return error_hint

        return inner  # type: ignore

    return decorator


def parse_input(user_input: str) -> tuple[str, list[str]]:
    cmd, *args = user_input.strip().split()
    return cmd.lower(), args


@input_error("Invalid command format. Usage: add <name> <phone number>")
def add_contact(args: list[str], book: AddressBook) -> str:
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
    return message


@input_error("Invalid command format. Usage: change <name> <old phone> <new phone>")
def change_contact(args: list[str], book: AddressBook) -> str:
    if len(args) != 3:
        raise IndexError
    name, old_phone, new_phone = args
    record = book.find(name)
    if record is None:
        return "Contact not found."
    if not record.edit_phone(old_phone, new_phone):
        return "Old phone number not found."
    return "Contact phone updated."


@input_error("Invalid command format. Usage: phone <name>")
def show_phone(args: list[str], book: AddressBook) -> str:
    if len(args) != 1:
        raise IndexError
    name = args[0]
    record = book.find(name)
    if record is None:
        return "Contact not found."
    return "; ".join(p.value for p in record.phones)


def show_all(book: AddressBook) -> str:
    if not book.data:
        return "No contacts saved."
    return "\n".join(str(record) for record in book.data.values())


@input_error("Invalid command format. Usage: add-birthday <name> <DD.MM.YYYY>")
def add_birthday(args: list[str], book: AddressBook) -> str:
    if len(args) != 2:
        raise IndexError
    name, bday = args
    record = book.find(name)
    if record is None:
        return "Contact not found."
    record.add_birthday(bday)
    return "Birthday added."


@input_error("Invalid command format. Usage: show-birthday <name>")
def show_birthday(args: list[str], book: AddressBook) -> str:
    if len(args) != 1:
        raise IndexError
    name = args[0]
    record = book.find(name)
    if record is None or record.birthday is None:
        return "Birthday not found."
    return record.birthday.value.strftime("%d.%m.%Y")


@input_error("birthdays command doesn't take any arguments")
def birthdays(args: list[str], book: AddressBook) -> str:
    result = book.get_upcoming_birthdays()
    if not result:
        return "No upcoming birthdays."
    return "\n".join(f"{entry['name']}: {entry['congratulation_date']}" for entry in result)


def main() -> None:
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(args, book))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
