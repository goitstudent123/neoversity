import urllib.parse

import matplotlib.pyplot as plt
import pandas as pd

__DEBUG_TOGGLE = False


def get_encoded_url() -> str:
    raw_url = (
        "https://uk.wikipedia.org/wiki/"
        "Населення_України#Коефіцієнт_народжуваності_в_регіонах_України_(1950—2019)"
    )
    return urllib.parse.quote(raw_url, safe=":/#()?=&")


def load_birth_rate_table(url: str) -> pd.DataFrame:
    tables = pd.read_html(url, thousands=" ", flavor="lxml")
    return next(t for t in tables if "2019" in t.columns)


def clean_birth_rate_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Replace dashes and fix decimal commas
    for col in df.columns[1:]:
        df[col] = df[col].astype(str).str.replace(",", ".", regex=False).replace("—", pd.NA)
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Drop summary row (last one, for all of Ukraine)
    df = df.iloc[:-1].copy()

    # Fill NaNs with column means
    df.fillna(df.mean(numeric_only=True), inplace=True)

    return df


def describe_dataframe(df: pd.DataFrame) -> None:
    print("=== First rows ===")
    print(df.head(), "\n")

    print("Shape:", df.shape, "\n")

    print("Dtypes:\n", df.dtypes, "\n")

    print("Missing value fractions:")
    print((df.isnull().sum() / len(df)).round(3), "\n")


def analyze_2019_high_regions(df: pd.DataFrame) -> None:
    mean_2019 = df["2019"].mean()
    high_regions = df.loc[df["2019"] > mean_2019, df.columns[0]]
    print("Regions with 2019 birth rate above national average:")
    print(high_regions.to_list(), "\n")


def find_max_region_2014(df: pd.DataFrame) -> None:
    if df["2014"].isnull().all():
        print("No data available for 2014.")
        return

    idx_max = df["2014"].idxmax(skipna=True)
    region = df.at[idx_max, df.columns[0]]
    print("Region with highest birth rate in 2014:", region, "\n")


def plot_birth_rate_2019(df: pd.DataFrame) -> None:
    df.plot(kind="bar", x=df.columns[0], y="2019", legend=False)
    plt.ylabel("Birth rate 2019")
    plt.title("2019 Birth Rates by Region")
    plt.tight_layout()
    plt.show()


def analyze_birth_rates() -> None:
    url = get_encoded_url()
    print(f"Encoded URL: {url}")

    raw_df = load_birth_rate_table(url)
    if __DEBUG_TOGGLE:
        describe_dataframe(raw_df)

    df = clean_birth_rate_data(raw_df)
    if __DEBUG_TOGGLE:
        describe_dataframe(df)

    analyze_2019_high_regions(df)
    find_max_region_2014(df)
    plot_birth_rate_2019(df)


if __name__ == "__main__":
    analyze_birth_rates()
