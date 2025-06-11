import re


def normalize_phone(phone_number: str) -> str:
    """
    Normalize a phone number to the format suitable for SMS sending.
    Keeps only digits and '+' at the beginning.
    Adds '+38' if international prefix is missing.

    :param phone_number: String containing a phone number in any format
    :return: Normalized phone number string starting with '+38'
    """
    phone_number = phone_number.strip()
    cleaned = re.sub(r"\D", "", phone_number)
    if phone_number.startswith("+"):
        return "+" + cleaned

    if cleaned.startswith("+"):
        return "+" + re.sub(r"\D", "", cleaned[1:])

    if cleaned.startswith("380"):
        return "+" + cleaned

    return "+38" + cleaned


if __name__ == "__main__":
    raw_numbers = [
        "067\\t123 4567",
        "(095) 234-5678\\n",
        "+380 44 123 4567",
        "380501234567",
        "    +38(050)123-32-34",
        "     0503451234",
        "(050)8889900",
        "38050-111-22-22",
        "38050 111 22 11   ",
    ]

    sanitized_numbers = [normalize_phone(num) for num in raw_numbers]
    print("Нормалізовані номери телефонів для SMS-розсилки:", sanitized_numbers)
