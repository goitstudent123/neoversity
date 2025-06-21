from io import StringIO

import pandas as pd
from _pytest.capture import CaptureFixture

from tier2.hw02.analyze_birth_rates import analyze_2019_high_regions, clean_birth_rate_data


def test_clean_birth_rate_data_handles_dashes_and_commas() -> None:
    raw_csv = """
              Регіон,1950,1960,1970,1990,2000,2012,2014,2019
              Рівненська,"23,5","—","19,0",13,7,"12,2","11,5","9,1"
              Київська,"22,0","20,0","18,0",12,8,"10,0","10,5","7,9"
              Вся Україна,"23,0","21,0","19,0",13,8,"12,0","11,0","10,0"
              """
    df = pd.read_csv(StringIO(raw_csv), dtype=str)
    cleaned = clean_birth_rate_data(df)

    assert cleaned.shape == (2, 9)
    assert cleaned["1950"].iloc[0] == 23.5
    assert cleaned["1960"].isna().sum() == 0
    assert round(cleaned["2019"].mean(), 2) == 8.5


def test_high_birth_rate_regions(capsys: CaptureFixture[str]) -> None:
    df = pd.DataFrame({"Регіон": ["A", "B", "C"], "2019": [9.0, 7.0, 10.0]})
    analyze_2019_high_regions(df)
    captured = capsys.readouterr()
    assert "A" in captured.out
    assert "C" in captured.out
    assert "B" not in captured.out
