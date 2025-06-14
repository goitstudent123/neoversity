# hw03.py
import sys
from pathlib import Path

from colorama import Fore, Style, init


def print_tree(path: Path, prefix: str = "") -> None:
    def print_folder(entry: Path) -> None:
        print_item(Fore.BLUE, entry.name + "/")

    def print_file(entry: Path) -> None:
        print_item(Fore.GREEN, entry.name)

    def print_item(color: str, name: str) -> None:
        print(f"{prefix}{color}{name}{Style.RESET_ALL}")

    if not path.exists():
        print(f"Path does not exist: {path}")
        return

    if not path.is_dir():
        print(f"Path is not a directory: {path}")
        return

    print_folder(path.resolve())
    entries = sorted(path.iterdir(), key=lambda p: p.name.lower())

    for index, entry in enumerate(entries):
        is_last = index == len(entries) - 1
        branch = "  " if not is_last else "   "
        prefix_next = prefix + branch

        if entry.is_dir():
            print_folder(entry)
            print_tree(entry, prefix_next)
        else:
            print_file(entry)


def main() -> None:
    init(autoreset=True)

    if len(sys.argv) != 2:
        print("Usage: python hw03.py /path/to/directory")
        sys.exit(1)

    path = Path(sys.argv[1])
    print_tree(path)


if __name__ == "__main__":
    main()
