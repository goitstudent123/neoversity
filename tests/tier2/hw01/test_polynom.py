from tier2.hw01.polynom import get_polynom


def test_polynom() -> None:
    coords = [(1, 12), (3, 54), (-1, 2)]
    c1, c2, c3 = get_polynom(coords)
    assert round(c1) == 3
    assert round(c2) == 5
    assert round(c3) == 4
