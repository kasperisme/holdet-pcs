import json
import pandas as pd
import requests


def loader(page: str):

    r = requests.get(
        "https://www.holdet.dk/handlers/tradedata.ashx?language=da&game=tour-de-france-2024&userteam=&partial-name=&positions=&team=&formation=cycling_trading_8_riders&minimum-value=0&maximum-value=0&lineup=&original-lineup=&sort=value&addable-only=false&direction=-1&page={}&include-headers=false&include-formations=false&include-lineup=false&include-fields=false&r=1719138842620".format(
            page
        )
    )
    d = r.json()

    values = [[i["Values"][2], i["Values"][16]] for i in d["Dataset"]["Items"]]

    return values


ls_filenames = ["holdet_1.json"]
values = []
for i in range(0, 6):
    values.extend(loader(i))

print(len(values))

pd.DataFrame(values, columns=["name", "price"]).to_excel("output/holdet.xlsx")
