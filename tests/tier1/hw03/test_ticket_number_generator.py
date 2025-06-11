from unittest.mock import patch

from tier1.hw03.ticket_number_generator import get_numbers_ticket


def test_valid() -> None:
    with patch("random.sample", return_value=[5, 2, 8, 3, 1, 4]):
        ticket = get_numbers_ticket(1, 49, 6)
        assert ticket == [1, 2, 3, 4, 5, 8]  # Sorted version


def test_min_equals_max() -> None:
    ticket = get_numbers_ticket(5, 5, 1)
    assert ticket == [5]


def test_invalid_range() -> None:
    assert get_numbers_ticket(50, 10, 5) == []


def test_quantity_too_large() -> None:
    assert get_numbers_ticket(1, 5, 10) == []


def test_min_too_low() -> None:
    assert get_numbers_ticket(0, 100, 5) == []


def test_max_too_high() -> None:
    assert get_numbers_ticket(1, 1001, 5) == []


def test_zero_quantity() -> None:
    assert get_numbers_ticket(1, 100, 0) == []


def test_full_range() -> None:
    with patch("random.sample", return_value=list(range(19, 9, -1))):
        ticket = get_numbers_ticket(10, 19, 10)
        assert ticket == list(range(10, 20))


if __name__ == "__main__":
    test_valid()
    test_min_equals_max()
    test_invalid_range()
    test_quantity_too_large()
    test_min_too_low()
    test_max_too_high()
    test_zero_quantity()
    test_full_range()
    print("✅ All tests passed for get_numbers_ticket")
