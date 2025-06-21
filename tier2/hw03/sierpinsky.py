import random

import matplotlib.pyplot as plt
import numpy as np


def midpoint(p1: np.ndarray, p2: np.ndarray) -> np.ndarray:
    return (p1 + p2) / 2


def generate_sierpinski(triangle: np.ndarray, num_points: int = 10000) -> np.ndarray:
    # Initial random point inside the triangle
    def random_point_inside(tri: np.ndarray) -> np.ndarray:
        s, t = sorted([random.random(), random.random()])
        a, b, c = tri
        return (1 - s) * a + (s - t) * b + t * c

    vertices = np.array(triangle)
    points = []

    current = random_point_inside(vertices)

    for _ in range(num_points):
        chosen_vertex = vertices[random.randint(0, 2)]
        current = midpoint(current, chosen_vertex)
        points.append(current)

    return np.array(points)


if __name__ == "__main__":
    triangle_vertices = np.array([[0, 0], [1, 0], [0.5, np.sqrt(3) / 2]])

    sierpinski_points = generate_sierpinski(triangle_vertices, num_points=50000)

    plt.figure(figsize=(6, 6))
    plt.plot(sierpinski_points[:, 0], sierpinski_points[:, 1], "k^", markersize=0.1)
    plt.title("Sierpiński triangle")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.axis("equal")
    plt.grid(True, which="both", linestyle=":", linewidth=0.3)
    plt.tight_layout()

    plt.show()
