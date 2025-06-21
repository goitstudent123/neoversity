import numpy as np

from tier2.hw01.deposits import solve_deposits


def test_solve_deposits_returns_correct_answer() -> None:
    b1, b2, b3 = solve_deposits()
    assert np.isclose(b1, 10000)
    assert np.isclose(b2, 25000)
    assert np.isclose(b3, 15000)


def test_solve_deposits_sum_is_correct() -> None:
    result = solve_deposits()
    total = np.sum(result)
    assert round(total, 2) == 50000


def test_solve_deposits_interest_1_and_2() -> None:
    x, y, _ = solve_deposits()
    interest = 0.05 * x + 0.07 * y
    assert round(interest, 2) == 2250


def test_solve_deposits_interest_1_and_3() -> None:
    x, _, z = solve_deposits()
    interest = 0.05 * x + 0.06 * z
    assert round(interest, 2) == 1400
