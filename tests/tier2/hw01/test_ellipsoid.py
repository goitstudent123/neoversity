from tier2.hw01.ellipsoid import solve_ellipsoid


def test_ellipsoid() -> None:
    a2, b2, c2 = solve_ellipsoid()
    assert round(a2) == 12
    assert round(b2) == 2
    assert round(c2) == 4
