import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import quad
from scipy.interpolate import interp1d


def generate_time_vector(start: float = 0, end: float = 11, num_points: int = 12) -> np.ndarray:
    return np.linspace(start, end, num_points)


def plot_observations(
    time: np.ndarray,
    speed: np.ndarray,
    xlim: tuple[float, float] = (0, 11),
    ylim: tuple[float, float] = (0, 130),
) -> None:
    plt.figure(figsize=(10, 6))
    plt.scatter(time, speed, color="blue", label="Speed observations")
    plt.xlim(*xlim)
    plt.ylim(*ylim)
    plt.grid(True)
    plt.title("Speed Observations")
    plt.xlabel("Time (hours)")
    plt.ylabel("Speed (km/h)")
    plt.legend()
    plt.show()


def interpolate_and_plot(
    time: np.ndarray,
    speed: np.ndarray,
    kind: str = "cubic",
    num_points: int = 10000,
    xlim: tuple[float, float] = (0, 11),
    ylim: tuple[float, float] = (0, 130),
) -> None:
    interp_func = interp1d(time, speed, kind=kind)
    dense_time = np.linspace(time[0], time[-1], num_points)
    dense_speed = interp_func(dense_time)

    plt.figure(figsize=(10, 6))
    plt.plot(dense_time, dense_speed, label=f"{kind.capitalize()} Interpolation")
    plt.scatter(time, speed, color="red", label="Original Data")
    plt.xlim(*xlim)
    plt.ylim(*ylim)
    plt.grid(True)
    plt.title(f"{kind.capitalize()} Interpolation of Speed Data")
    plt.xlabel("Time (hours)")
    plt.ylabel("Speed (km/h)")
    plt.legend()
    plt.show()

    integral, _ = quad(interp_func, time[0], time[-1])


if __name__ == "__main__":
    speed = np.array([25, 35, 45, 30, 60, 120, 100, 100, 70, 75, 80, 65])
    time = generate_time_vector()

    # Plot original observations
    plot_observations(time, speed)

    # Interpolation and integration
    for kind in ["linear", "cubic", "quadratic"]:
        interpolate_and_plot(time, speed, kind=kind)
