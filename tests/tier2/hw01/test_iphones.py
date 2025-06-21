import numpy as np

from tier2.hw01.iphones import solve_iphone_stock


def test_solve_iphone_stock_values() -> None:
    x, y, z = solve_iphone_stock()
    assert np.isclose(x, 436)
    assert np.isclose(y, 556)
    assert np.isclose(z, 336)


def test_total_stock_sum() -> None:
    x, y, z = solve_iphone_stock()
    assert round(x + y + z) == 1328


def test_relative_12_and_13() -> None:
    x, y, _ = solve_iphone_stock()
    assert round(y - x) == 120


def test_relative_12_and_15() -> None:
    x, _, z = solve_iphone_stock()
    assert round(x - z) == 100
