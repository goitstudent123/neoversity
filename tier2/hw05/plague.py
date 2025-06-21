from typing import Callable, Union

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import interp1d
from scipy.optimize import curve_fit, minimize_scalar

ArrayLike = Union[float, np.ndarray]


class Parameters:
    alpha: float = 0.5
    beta: float = 0.3
    population: int = 1_000_000
    susceptible_init: int = 990_000
    infected_init: int = 7_000
    recovered_init: int = 3_000
    time_start: float = 0.0
    time_end: float = 25.0
    time_points: np.ndarray = np.linspace(time_start, time_end, 500)


def sir_derivatives(_: float, state: list[float]) -> list[float]:
    s, i = state
    ds_dt = -Parameters.alpha * s
    di_dt = Parameters.alpha * s - Parameters.beta * i
    return [ds_dt, di_dt]


def compute_sir() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    result = solve_ivp(
        fun=sir_derivatives,
        t_span=[Parameters.time_start, Parameters.time_end],
        y0=[Parameters.susceptible_init, Parameters.infected_init],
        t_eval=Parameters.time_points,
    )
    s, i = result.y
    r = Parameters.population - s - i
    return result.t, s, i, r


def fit_susceptible_model(
    t: np.ndarray, s: np.ndarray
) -> tuple[Callable[[np.ndarray], np.ndarray], np.ndarray]:
    def model(t: np.ndarray, s0: float, alpha: float) -> np.ndarray:
        return s0 * np.exp(-alpha * t)

    params, _ = curve_fit(model, t, s, p0=(Parameters.susceptible_init, Parameters.alpha))
    return lambda x: model(x, *params), params


def fit_infected_model(
    t: np.ndarray, i: np.ndarray
) -> tuple[Callable[[np.ndarray], np.ndarray], np.ndarray]:
    def model(t: np.ndarray, i0: float, alpha: float, s0: float) -> np.ndarray:
        return (i0 + alpha * s0 * t) * np.exp(-alpha * t)

    params, _ = curve_fit(
        model, t, i, p0=(Parameters.infected_init, Parameters.alpha, Parameters.susceptible_init)
    )
    return lambda x: model(x, *params), params


def compute_recovered_interp(
    s_interp: Callable[[ArrayLike], ArrayLike],
    i_interp: Callable[[ArrayLike], ArrayLike],
) -> Callable[[ArrayLike], ArrayLike]:
    def recovered(x: ArrayLike) -> ArrayLike:
        return Parameters.population - s_interp(x) - i_interp(x)

    return recovered


def compute_recovered_fit(
    s_fit: Callable[[ArrayLike], ArrayLike],
    i_fit: Callable[[ArrayLike], ArrayLike],
) -> Callable[[ArrayLike], ArrayLike]:
    def recovered(x: ArrayLike) -> ArrayLike:
        return Parameters.population - s_fit(x) - i_fit(x)

    return recovered


def find_peak_infection(i_func: Callable[[float], float]) -> tuple[float, float]:
    result = minimize_scalar(
        lambda t: -i_func(t), bounds=(Parameters.time_start, Parameters.time_end), method="bounded"
    )
    return result.x, i_func(result.x)


def plot_sir(
    t: np.ndarray,
    s: np.ndarray,
    i: np.ndarray,
    r: np.ndarray,
    s_fit: Callable[[np.ndarray], np.ndarray],
    i_fit: Callable[[np.ndarray], np.ndarray],
    r_fit: Callable[[np.ndarray], np.ndarray],
) -> None:
    plt.figure(figsize=(12, 6))
    plt.plot(t, s, label="Susceptible (actual)", linewidth=2)
    plt.plot(t, i, label="Infected (actual)", linewidth=2)
    plt.plot(t, r, label="Recovered (actual)", linewidth=2)

    plt.plot(t, s_fit(t), "--", label="Susceptible (fitted)")
    plt.plot(t, i_fit(t), "--", label="Infected (fitted)")
    plt.plot(t, r_fit(t), "--", label="Recovered (fitted)")

    plt.xlabel("Time")
    plt.ylabel("Individuals")
    plt.title("SIR Model: Actual vs Fitted")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    t, s_actual, i_actual, r_actual = compute_sir()

    s_interp = interp1d(t, s_actual, kind="cubic")
    i_interp = interp1d(t, i_actual, kind="cubic")

    r_interp = compute_recovered_interp(s_interp, i_interp)

    s_fit, _ = fit_susceptible_model(t, s_actual)
    i_fit, _ = fit_infected_model(t, i_actual)
    r_fit = compute_recovered_fit(s_fit, i_fit)

    t_peak, i_peak = find_peak_infection(i_fit)

    print(f"📈 Peak infection at t = {t_peak:.2f}, I(t) = {int(i_peak)}")
    plot_sir(t, s_actual, i_actual, r_actual, s_fit, i_fit, r_fit)
