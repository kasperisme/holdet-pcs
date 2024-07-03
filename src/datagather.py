import pandas as pd
import os


def merge_df(
    price: pd.DataFrame,
    riders: pd.DataFrame,
    odds: pd.DataFrame,
    outputpath: str = "output",
):

    # Cleaning names
    price["name"] = price["name"].apply(lambda x: x.title())
    riders["name"] = riders["name"].apply(lambda x: x.title())
    odds["name"] = odds["name"].apply(lambda x: x.title())

    # Replacements

    list_replacements = [
        {"old": "Casper Phillip Pedersen", "new": "Casper Pedersen"},
        {"old": "Enric Mas Nicolau", "new": "Enric Mas"},
        {"old": "Jesus Herrada Lopez", "new": "Jesus Herrada"},
        {"old": "Ion Izagirre Insausti", "new": "Ion Izagirre"},
        {"old": " ", "new": ""},
        {"old": "é", "new": "e"},
        {"old": "á", "new": "a"},
        {"old": "ó", "new": "o"},
        {"old": "ñ", "new": "n"},
        {"old": "ç", "new": "c"},
        {"old": "ã", "new": "a"},
        {"old": "ú", "new": "u"},
        {"old": "í", "new": "i"},
        {"old": "ł", "new": "l"},
        {"old": "ü", "new": "u"},
        {"old": "ä", "new": "a"},
        {"old": "-", "new": ""},
        {"old": "ž", "new": "z"},
        {"old": "č", "new": "c"},
    ]

    # Apply replacements
    for replacement in list_replacements:
        price["name"] = price["name"].apply(
            lambda x: x.replace(replacement["old"], replacement["new"])
        )
        riders["name"] = riders["name"].apply(
            lambda x: x.replace(replacement["old"], replacement["new"])
        )
        odds["name"] = odds["name"].apply(
            lambda x: x.replace(replacement["old"], replacement["new"])
        )
    # Merge
    riders_budget = riders.merge(price, how="left", left_on="name", right_on="name")
    riders_budget = riders_budget.merge(
        odds, how="left", left_on="name", right_on="name"
    )

    riders_budget["odds"] = riders_budget["odds"].fillna(
        min(riders_budget["odds"]) * 1.5
    )

    # Save
    riders_budget.to_excel(os.path.join(outputpath, "riders_budget.xlsx"))

    return riders_budget


def main(outputpath: str = "output", readpath: str = "output"):
    price = pd.read_excel(os.path.join(readpath, "holdet.xlsx"))
    riders = pd.read_excel(
        os.path.join(readpath, "riders_stagepotential_analysis.xlsx")
    )
    odds = pd.read_excel(os.path.join(readpath, "odds.xlsx"))
    merge_df(price, riders, odds, outputpath)


if __name__ == "__main__":
    main()
