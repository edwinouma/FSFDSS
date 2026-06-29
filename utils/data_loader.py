import pandas as pd

DATA_PATH = "data/historical_data.csv"


def load_data():

    df = pd.read_csv(DATA_PATH)

    # Create chronological order
    season_order = {
        "Gu": 1,
        "Deyr": 2
    }

    df["season_order"] = df["season"].map(season_order)

    df = df.sort_values(
        ["year", "season_order"]
    )

    df["Period"] = (
        df["year"].astype(str)
        + " "
        + df["season"]
    )

    return df