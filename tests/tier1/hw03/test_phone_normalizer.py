from tier1.hw03.phone_normalizer import normalize_phone


def test_tab_and_spaces() -> None:
    assert normalize_phone("067\t123 4567") == "+380671234567"


def test_parentheses_and_newline() -> None:
    assert normalize_phone("(095) 234-5678\n") == "+380952345678"


def test_plus_and_spaces() -> None:
    assert normalize_phone("+380 44 123 4567") == "+380441234567"


def test_starts_with_380() -> None:
    assert normalize_phone("380501234567") == "+380501234567"


def test_plus_brackets_dashes() -> None:
    assert normalize_phone("    +38(050)123-32-34") == "+380501233234"


def test_plain_number() -> None:
    assert normalize_phone("     0503451234") == "+380503451234"


def test_parentheses_only() -> None:
    assert normalize_phone("(050)8889900") == "+380508889900"


def test_dashes() -> None:
    assert normalize_phone("38050-111-22-22") == "+380501112222"


def test_spaces_at_end() -> None:
    assert normalize_phone("38050 111 22 11   ") == "+380501112211"
