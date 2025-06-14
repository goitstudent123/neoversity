import textwrap

from tier1.hw05.profit_parser import generator_numbers, sum_profit


def test_generator_numbers_basic() -> None:
    text = " 100.00 and then 50.50 are incomes "
    result = list(generator_numbers(text))
    assert result == [100.00, 50.50], f"Unexpected result: {result}"


def test_generator_numbers_with_punctuation() -> None:
    text = "Revenue:  1000.01 , bonus 27.45 ."
    result = list(generator_numbers(text))
    assert result == [1000.01, 27.45], f"Unexpected result: {result}"


def test_generator_numbers_ignores_embedded() -> None:
    text = "Income100.01 is invalid, but 100.01 is valid"
    result = list(generator_numbers(text))
    assert result == [100.01], f"Unexpected result: {result}"


def test_sum_profit_example() -> None:
    text = textwrap.dedent(
        """
        Загальний дохід працівника складається з декількох частин: 
        1000.01 як основний дохід, 
        доповнений додатковими надходженнями 27.45 і 324.00 доларів.
    """
    ).strip()
    total = sum_profit(text, generator_numbers)
    assert abs(total - 1351.46) < 0.001, f"Expected 1351.46, got {total}"


def test_sum_profit_empty() -> None:
    text = "No numbers here."
    total = sum_profit(text, generator_numbers)
    assert total == 0.0, f"Expected 0.0, got {total}"


def test_sum_profit_only_one_number() -> None:
    text = " The income is 99.99 only."
    total = sum_profit(text, generator_numbers)
    assert abs(total - 99.99) < 0.001, f"Expected 99.99, got {total}"


if __name__ == "__main__":
    test_generator_numbers_basic()
    test_generator_numbers_with_punctuation()
    test_generator_numbers_ignores_embedded()
    test_sum_profit_example()
    test_sum_profit_empty()
    test_sum_profit_only_one_number()
    print("\u2705 All tests passed for generator_numbers and sum_profit")
