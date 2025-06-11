import os

from tier1.hw04.salary_calculator import total_salary


def test_basic_valid_file() -> None:
    test_path = "test_salary.txt"
    with open(test_path, "w", encoding="utf-8") as f:
        f.write("Alex Korp,3000\n")
        f.write("Nikita Borisenko,2000\n")
        f.write("Sitarama Raju,1000\n")

    total, avg = total_salary(test_path)
    assert total == 6000
    assert avg == 2000.0

    os.remove(test_path)


def test_empty_file() -> None:
    test_path = "empty_salary.txt"
    with open(test_path, "w", encoding="utf-8"):
        pass

    total, avg = total_salary(test_path)
    assert total == 0
    assert avg == 0.0

    os.remove(test_path)


def test_file_with_invalid_lines() -> None:
    test_path = "invalid_lines.txt"
    with open(test_path, "w", encoding="utf-8") as f:
        f.write("John Doe,1000\n")
        f.write("BadLineWithoutComma\n")
        f.write("Jane Smith,2000\n")
        f.write("NoNumber,abc\n")

    total, avg = total_salary(test_path)
    assert total == 3000
    assert avg == 1500.0

    os.remove(test_path)


def test_missing_file() -> None:
    try:
        total_salary("no_such_file.txt")
        assert False, "Expected FileNotFoundError"
    except FileNotFoundError:
        pass


def test_file_with_whitespace() -> None:
    test_path = "whitespace.txt"
    with open(test_path, "w", encoding="utf-8") as f:
        f.write("   John Smith,1000  \n")
        f.write("Alice Moore,  2000\n")

    total, avg = total_salary(test_path)
    assert total == 3000
    assert avg == 1500.0

    os.remove(test_path)
