from typing import Callable


def caching_fibonacci(cache: dict[int, int] = {}) -> Callable[[int], int]:
    def fibonacci(n: int) -> int:
        if n in cache:
            return cache[n]
        if n <= 1:
            cache[n] = n
        else:
            cache[n] = fibonacci(n - 1) + fibonacci(n - 2)
        return cache[n]

    return fibonacci


if __name__ == "__main__":
    fib = caching_fibonacci()
    print(fib(10))  # Виведе 55
    print(fib(15))  # Виведе 610
