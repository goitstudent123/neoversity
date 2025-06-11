import re
import textwrap
from typing import Callable, Generator


def generator_numbers(text: str) -> Generator[float, None, None]:
    for match in re.findall(r"(?<=\s)(\d+\.\d+)(?=\s)", f" {text} "):
        yield float(match)


def sum_profit(text: str, func: Callable[[str], Generator[float, None, None]]) -> float:
    return sum(func(text))


def main() -> None:
    text = textwrap.dedent(
        """
        Загальний дохід працівника складається з декількох частин: 
        1000.01 як основний дохід, доповнений додатковими надходженнями 
        27.45 і 324.00 доларів.
    """
    ).strip()
    total_income = sum_profit(text, generator_numbers)
    print(f"Загальний дохід: {total_income}")  # 1351.46


if __name__ == "__main__":
    main()
