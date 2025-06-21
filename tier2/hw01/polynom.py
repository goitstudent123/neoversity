from typing import Sequence, Tuple

import numpy as np


def get_polynom(coords: Sequence[Tuple[float, float]]) -> np.ndarray:
    n = len(coords) - 1  # degree of the polynomial
    x_vals = np.array([x for x, _ in coords])
    y_vals = np.array([y for _, y in coords])

    # Construct Vandermonde matrix: rows of [1, x, x^2, ..., x^n]
    A = np.vander(x_vals, N=n + 1, increasing=True)

    return np.linalg.solve(A, y_vals)


if __name__ == "__main__":
    coords = [(1, 12), (3, 54), (-1, 2)]
    coefficients = get_polynom(coords)
    print(coefficients)
