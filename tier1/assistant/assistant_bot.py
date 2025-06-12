from typing import Any, Callable, TypeVar

F = TypeVar("F", bound=Callable[..., Any])


def input_error(error_hint: str = "Enter the argument for the command") -> Callable[[F], F]:
    def decorator(func: F) -> F:
        def inner(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except KeyError:
                return "Contact not found."
            except ValueError:
                return error_hint
            except IndexError:
                return error_hint

        return inner  # type: ignore

    return decorator


def parse_input(user_input: str) -> tuple[str, list[str]]:
    cmd, *args = user_input.strip().split()
    return cmd.lower(), args


@input_error("Invalid command format. Usage: add <name> <phone number>")
def add_contact(args: list[str], contacts: dict[str, str]) -> str:
    if len(args) != 2:
        raise IndexError
    name, phone = args
    contacts[name] = phone
    return "Contact added."


@input_error("Invalid command format. Usage: change <name> <phone number>")
def change_contact(args: list[str], contacts: dict[str, str]) -> str:
    if len(args) != 2:
        raise IndexError
    name, phone = args
    if name in contacts:
        contacts[name] = phone
        return "Contact updated."
    return "Contact not found."


@input_error("Invalid command format. Usage: phone <name>")
def show_phone(args: list[str], contacts: dict[str, str]) -> str:
    if len(args) != 1:
        raise IndexError
    name = args[0]
    return contacts[name]


def show_all(contacts: dict[str, str]) -> str:
    if not contacts:
        return "No contacts saved."
    return "\n".join(f"{name}: {phone}" for name, phone in contacts.items())


def main() -> None:
    contacts: dict[str, str] = {}
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
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "all":
            print(show_all(contacts))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
