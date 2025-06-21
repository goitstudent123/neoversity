import numpy as np
from numpy.typing import NDArray


def solve_iphone_stock(total: int = 1328) -> NDArray[np.float64]:
    # Variables: x = iPhone12, y = iPhone13, z = iPhone15
    A = np.array(
        [
            [1, 1, 1],  # x + y + z = 1328
            [1, -1, 0],  # x - y = -120
            [1, 0, -1],  # x - z = 100
        ]
    )
    b = np.array([total, -120, 100])
    return np.linalg.solve(A, b)


if __name__ == "__main__":
    x, y, z = solve_iphone_stock()
    print(f"iPhone12 stock: {x}")
    print(f"iPhone13 stock: {y}")
    print(f"iPhone14 stock: {z}")
    print(f"Total iPhone stock: {round(x) + round(y) + round(z)} (1328 expected)")
    print(f"iPhone12 - iPhone13 = {round(y - x)} (120 expected)")
    print(f"iPhone12 - iPhone15 = {round(x - z)} (100 expected)")
