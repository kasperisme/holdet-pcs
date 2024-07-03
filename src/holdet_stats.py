import requests
import pandas as pd
import os
from sklearn.preprocessing import StandardScaler


def loader(round: str):
    """Load data from holdet.dk
    Args:
        page (str): page number

    Returns:
        list: list of values
    """
    r = requests.get(
        "https://api.holdet.dk/games/696/rounds/{}/statistics?appid=holdet&culture=da-DK".format(
            round
        )
    )
    d = r.json()

    df = pd.DataFrame(d)

    df = pd.concat(
        [
            df.drop(["player"], axis=1),
            df["player"].apply(pd.Series),
        ],
        axis=1,
    )

    df = df.rename(columns={"id": "player_id"})

    df = pd.concat(
        [
            df.drop(["values"], axis=1),
            df["values"].apply(pd.Series),
        ],
        axis=1,
    )

    df = pd.concat(
        [
            df.drop(["events"], axis=1),
            df["events"].apply(pd.Series),
        ],
        axis=1,
    )

    df = df.rename(columns={"id": "round_id"})

    cols = ["popularity", "trend", "index", "totalGrowth"]

    scaler = StandardScaler()

    df[cols] = scaler.fit_transform(df[cols].to_numpy())

    return df


def main(outputpath: str = "output", round: int = 0):
    df = loader(str(round + 1))

    df.to_excel(os.path.join(outputpath, "holdet_stats.xlsx"))

    return df


if __name__ == "__main__":
    main(round=4)
