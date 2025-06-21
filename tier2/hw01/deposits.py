import numpy as np
from numpy._typing import NDArray


def solve_deposits(
    total: float = 50000,
    r1: float = 0.05,
    r2: float = 0.07,
    r3: float = 0.06,
    i12: float = 2250,
    i13: float = 1400,
) -> NDArray[np.float64]:
    # Let x = deposit in bank1, y = bank2, z = bank3
    # x + y + z = total
    # 0.05x + 0.07y         = 2250
    # 0.05x         + 0.06z = 1400

    A = np.array([[1, 1, 1], [r1, r2, 0], [r1, 0, r3]])
    b = np.array([total, i12, i13])

    return np.linalg.solve(A, b)


if __name__ == "__main__":
    r1 = 0.05
    r2 = 0.07
    r3 = 0.06
    b1, b2, b3 = solve_deposits(
        total=50000,
        r1=r1,
        r2=r2,
        r3=r3,
        i12=2250,
        i13=1400,
    )
    income1 = round(r1 * b1)
    income2 = round(r2 * b2)
    income3 = round(r3 * b3)
    print(f"First bank deposit: {round(b1)}, interest rate is {r1}%, income: {income1}")
    print(f"First bank deposit: {round(b2)}, interest rate is {r2}%, income: {income2}")
    print(f"First bank deposit: {round(b3)}, interest rate is {r3}%, income: {income3}")
    print(f"1+2 income is {income1 + income2}, expected 2250")
    print(f"1+3 income is {income1 + income3}, expected 1400")
