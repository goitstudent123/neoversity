from tier2.hw01.porabola import solve_parabola


def test_parabola() -> None:
    a, b, c = solve_parabola()
    assert round(a) == 4
    assert round(b) == 5
    assert round(c) == 3
