import numpy as np


def solve_parabola(
    p1: tuple[float, float] = (1, 12),
    p2: tuple[float, float] = (3, 54),
    p3: tuple[float, float] = (-1, 2),
) -> tuple[float, float, float]:
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3

    A = np.array(
        [
            [x1**2, x1, 1],
            [x2**2, x2, 1],
            [x3**2, x3, 1],
        ]
    )
    B = np.array([y1, y2, y3])

    a, b, c = np.linalg.solve(A, B)
    return a, b, c


if __name__ == "__main__":
    a, b, c = solve_parabola()
    print(f"y = {a:.2f}·x^2 + {b:.2f}·x + {c:.2f}")
