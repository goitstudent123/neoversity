from tier1.hw05.fibonacci import caching_fibonacci


def test_fibonacci_base_cases() -> None:
    fib = caching_fibonacci()
    assert fib(0) == 0
    assert fib(1) == 1


def test_fibonacci_small_numbers() -> None:
    fib = caching_fibonacci()
    assert fib(2) == 1
    assert fib(3) == 2
    assert fib(4) == 3
    assert fib(5) == 5
    assert fib(6) == 8


def test_fibonacci_medium() -> None:
    fib = caching_fibonacci()
    assert fib(10) == 55
    assert fib(15) == 610
    assert fib(20) == 6765


def test_fibonacci_cache() -> None:
    cache: dict[int, int] = {}
    fib = caching_fibonacci(cache)
    fib(6)
    for n in range(7):
        assert n in cache
        assert cache[n] == fib(n)
