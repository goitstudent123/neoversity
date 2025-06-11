import random


def get_numbers_ticket(min_value: int, max_value: int, quantity: int) -> list[int]:
    """
    Generates a list of unique random numbers within a specified range for a lottery ticket.

    :param min_value: The minimum possible number (inclusive). Must be >= 1.
    :param max_value: The maximum possible number (inclusive). Must be <= 1000.
    :param quantity: Number of unique numbers to generate. Must be between min_value and max_value.
    :return: Sorted list of unique random numbers, or empty list if inputs are invalid.
    """
    if not (1 <= min_value <= max_value <= 1000):
        return []
    if not (0 < quantity <= (max_value - min_value + 1)):
        return []

    numbers = random.sample(range(min_value, max_value + 1), quantity)
    return sorted(numbers)


if __name__ == "__main__":
    lottery_numbers = get_numbers_ticket(1, 49, 6)
    print("Ваші лотерейні числа:", lottery_numbers)
