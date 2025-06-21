# Plot 3-5 different styled graphs for each problem
import random

import numpy as np
from matplotlib import pyplot as plt

from tier2.hw01.deposits import solve_deposits
from tier2.hw01.ellipsoid import solve_ellipsoid
from tier2.hw01.iphones import solve_iphone_stock
from tier2.hw01.polynom import get_polynom
from tier2.hw01.porabola import solve_parabola


def random_style() -> dict[str, str | float]:
    colors = ["blue", "green", "red", "purple", "orange", "black", "cyan", "magenta"]
    linestyles = ["-", "--", "-.", ":"]
    markers = ["o", "s", "^", "*", ".", "x", "D", "None"]
    linewidth = random.uniform(0.5, 1)

    return {
        "color": random.choice(colors),
        "linestyle": random.choice(linestyles),
        "marker": random.choice(markers),
        "linewidth": linewidth,
    }


def plot_parabola() -> None:
    plt.figure()
    x = np.linspace(-10, 10, 400)
    a, b, c = solve_parabola()
    y_par = a * x**2 + b * x + c
    plt.plot(x, y_par, label="Parabola", color="orange")
    plt.fill_between(x, y_par, color="orange", alpha=0.1)
    plt.title("Parabola from 3 points")
    plt.legend()
    plt.tight_layout()


def plot_polynomial() -> None:
    plt.figure()
    x = np.linspace(-10, 10, 400)
    coords = [(1, 12), (3, 54), (-1, 2)]
    coeffs = get_polynom(coords)
    y_poly = sum(c * x**i for i, c in enumerate(coeffs))
    plt.plot(x, y_poly, label="Polynomial", color="purple")
    plt.scatter(*zip(*coords), color="black", zorder=5)
    plt.title("Interpolated Polynomial")
    plt.legend()


def plot_deposits() -> None:
    plt.figure()
    x = np.linspace(-10, 10, 400)
    b1, b2, b3 = solve_deposits()
    y1 = b1 * 0.05 + x * 0.0001
    y2 = b2 * 0.07 + np.sin(x)
    y3 = b3 * 0.06 + np.log(np.abs(x) + 1)
    plt.plot(x, y1, label="Bank 1", **random_style())
    plt.plot(x, y2, label="Bank 2", **random_style())
    plt.plot(x, y3, label="Bank 3", **random_style())
    plt.title("Deposits: income functions")

    if random.random() < 0.5:
        plt.grid(True)
    if random.random() < 0.3:
        plt.gca().set_facecolor(random.choice(["#f0f0f0", "#fffaf0", "#f0ffff"]))

    plt.legend()


def plot_ellipsoid() -> None:
    plt.figure()
    a2, b2_, c2 = solve_ellipsoid()
    t = np.linspace(0, 2 * np.pi, 300)
    plt.plot(np.sqrt(a2) * np.cos(t), np.sqrt(b2_) * np.sin(t), label="XY projection")
    plt.plot(
        np.sqrt(a2) * np.cos(t), np.sqrt(c2) * np.sin(t), linestyle="dotted", label="XZ projection"
    )
    plt.title("Ellipsoid Projections")
    plt.axis("equal")
    plt.legend()


def plot_iphones() -> None:
    plt.figure()
    x_vals = np.arange(3)
    iphones = solve_iphone_stock()
    plt.bar(x_vals, iphones, tick_label=["iPhone12", "iPhone13", "iPhone15"])
    plt.title("iPhone Stock")
    plt.grid(True, axis="y")


if __name__ == "__main__":
    plot_deposits()
    plot_ellipsoid()
    plot_iphones()
    plot_polynomial()
    plot_parabola()

    plt.show()
