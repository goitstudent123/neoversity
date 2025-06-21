from scipy.optimize import OptimizeResult, minimize


def fence_length(args: tuple[float, float]) -> float:
    width, height = args
    return width + 2 * height


def calculate_minimum_fence_length(side: float = 1000.0) -> OptimizeResult:
    constraints = {"type": "eq", "fun": lambda args: args[0] * args[1] - side}
    x_bounds = (0, side)
    y_bounds = (0, side)
    bounds = (x_bounds, y_bounds)
    return minimize(fence_length, [1, side - 1], bounds=bounds, constraints=constraints)


if __name__ == "__main__":
    result = calculate_minimum_fence_length(side=1000.0)
    print(result.x)
