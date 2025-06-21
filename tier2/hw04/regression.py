from itertools import combinations

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Константи для зручності
OBS = "observation"
A, B, C = "A", "B", "C"
INCOME_COLS = [A, B, C]


def get_data() -> pd.DataFrame:
    return pd.DataFrame(
        {
            OBS: [1, 2, 3, 4, 5, 6],
            A: [25, -10, 10, 5, 35, 13],
            B: [0, 15, -5, 5, 20, 25],
            C: [10, 25, -15, -5, -5, 15],
        }
    )


def plot_regression(df: pd.DataFrame = None) -> None:
    if df is None:
        df = get_data()

    def add_subplot(position: int, x: str, y: str) -> None:
        plt.subplot(1, 3, position)
        sns.regplot(x=x, y=y, data=df)
        plt.xlabel(f"Прибутковість {x}, %")
        plt.ylabel(f"Прибутковість {y}, %")
        plt.title(f"Регресія: {x} vs {y}")

    plt.figure(figsize=(15, 5))

    for i, (x, y) in enumerate(combinations(INCOME_COLS, 2), start=1):
        add_subplot(i, x, y)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    plot_regression()
