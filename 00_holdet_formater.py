import pandas as pd
import requests


def loader(page: str):
    """Load data from holdet.dk
    Args:
        page (str): page number

    Returns:
        list: list of values
    """
    r = requests.get(
        "https://www.holdet.dk/handlers/tradedata.ashx?language=da&game=tour-de-france-2024&userteam=&partial-name=&positions=&team=&formation=cycling_trading_8_riders&minimum-value=0&maximum-value=0&lineup=&original-lineup=&sort=value&addable-only=false&direction=-1&page={}&include-headers=false&include-formations=false&include-lineup=false&include-fields=false&r=1719138842620".format(
            page
        )
    )
    d = r.json()

    values = [[i["Values"][2], i["Values"][16]] for i in d["Dataset"]["Items"]]

    return values


def main():
    values = []
    for i in range(0, 6):
        values.extend(loader(i))

    df = pd.DataFrame(values, columns=["name", "price"])

    df.to_excel("output/holdet.xlsx")

    return df


if __name__ == "__main__":
    main()
