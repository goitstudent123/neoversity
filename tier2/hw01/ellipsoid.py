from math import sqrt

import numpy as np


def solve_ellipsoid(
    a: tuple[float, float, float] = (sqrt(3), 0, sqrt(3)),
    b: tuple[float, float, float] = (sqrt(6), 1 / 2, 0),
    c: tuple[float, float, float] = (1, 1 / sqrt(3), 1),
) -> tuple[float, float, float]:
    A = np.array(
        [
            [a[0] ** 2, a[1] ** 2, a[2] ** 2],
            [b[0] ** 2, b[1] ** 2, b[2] ** 2],
            [c[0] ** 2, c[1] ** 2, c[2] ** 2],
        ]
    )
    b = np.array([1, 1, 1])

    # Solve for [1/a^2, 1/b^2, 1/c^2]
    X, Y, Z = np.linalg.solve(A, b)

    return __norm(1 / X), __norm(1 / Y), __norm(1 / Z)


def __norm(x: float) -> float:
    """
    Normalizes the input value based on its magnitude. The function returns the
    input value if its absolute value is greater than 1.0. Otherwise, it returns
    the reciprocal of the input value.

    :param x: Input floating-point number to be normalized.
    :type x: float
    :return: Normalized floating-point number.
    :rtype: float
    """
    return x if abs(x) > 1.0 else 1 / x


if __name__ == "__main__":
    a2, b2, c2 = solve_ellipsoid()
    print(f"Canonical equation:\n x^2/{a2:.3f} + y^2/{b2:.3f} + z^2/{c2:.3f} = 1")
