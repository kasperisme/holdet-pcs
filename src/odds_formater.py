import pandas as pd
import requests
import os
from sklearn.preprocessing import StandardScaler


def loader(etape: str):
    """Load data from holdet.dk
    Args:
        page (str): page number

    Returns:
        list: list of values
    """
    r = requests.get(
        "https://content.sb.danskespil.dk/content-service/api/v1/q/event-list?eventSortsIncluded=TNMT&includeChildMarkets=true&drilldownTagIds=19794"
    )
    d = r.json()

    name_ls = [i["name"] for i in d["data"]["events"]]

    index = name_ls.index("Tour de France 2024: {}. Etape - Vinder".format(etape))

    if index == -1:
        raise ValueError("Etape not found")

    df = pd.DataFrame(d["data"]["events"][index]["markets"][0]["outcomes"])

    df = pd.concat(
        [
            df.drop(["prices"], axis=1),
            df["prices"].apply(pd.Series),
        ],
        axis=1,
    )

    df = pd.concat(
        [
            df.drop([0], axis=1),
            df[0].apply(pd.Series),
        ],
        axis=1,
    )

    df = df[["name", "decimal"]]
    df = df.rename(columns={"decimal": "odds"})

    scaler = StandardScaler()

    df[["odds"]] = scaler.fit_transform(df[["odds"]].to_numpy() * -1)

    return df


def main(outputpath: str = "output", round: int = 0):
    df = loader(round + 1)

    df.to_excel(os.path.join(outputpath, "odds.xlsx"))
    return None


if __name__ == "__main__":
    main(round=4)
