import numpy as np
from scipy import optimize
import pandas as pd
import os


def mip_optimize(df_riders: pd.DataFrame, params: dict, outputpath: str = "output"):
    starting_stage = params["starting_stage"]
    capacity = params["capacity"]
    max_riders = params["max_riders"]

    sizes = df_riders["price"].values
    # applying weights to popularity and totalGrowth as these are historical values
    # while stage potential is based on the stage profile and rider fit
    # and trend is the wishdom of the crowd
    values = (
        df_riders[f"{starting_stage}_potential"].values
        + df_riders["popularity"].values * 0.8
        + df_riders["trend"].values
        + df_riders["totalGrowth"].values * 0.8
        + df_riders["odds"].values
    )

    bounds = optimize.Bounds(0, 1)  # 0 <= x_i <= 1
    integrality = np.full_like(values, True)  # x_i are integers
    capactiy_constraint = optimize.LinearConstraint(A=sizes, lb=0, ub=capacity)

    max_riders_constraint = optimize.LinearConstraint(
        A=np.ones_like(sizes), lb=max_riders, ub=max_riders
    )  # ensure that we have max_riders riders

    constraints = [capactiy_constraint, max_riders_constraint]

    res = optimize.milp(
        c=-values, constraints=constraints, integrality=integrality, bounds=bounds
    )

    df_riders["team"] = df_riders["teams_history"].apply(
        lambda x: x[x.find("'season': 2024") + 30 :][: x.find("'season': 2023")]
    )

    df_riders["selected"] = res.x.round().astype(int)
    df_riders["combined_potential"] = values
    df_riders["potential/DKK"] = df_riders["combined_potential"] / (
        df_riders["price"] / 10**7
    )

    print("Solved:", res.success)

    cols = [
        "name",
        "price",
        "combined_potential",
        f"{starting_stage}_potential",
        "popularity",
        "trend",
        "totalGrowth",
        "odds",
        "team",
        "potential/DKK",
        "selected",
    ]

    df_riders[cols].to_excel(os.path.join(outputpath, "riders_budget_selected.xlsx"))

    print(df_riders[df_riders["selected"] == 1][cols])

    print("Total cost:", df_riders[df_riders["selected"] == 1]["price"].sum())


def main(
    starting_stage: int = 0,
    capacity: int = 50000000,
    max_riders: int = 8,
    read_path: str = "output",
):
    params = {
        "starting_stage": starting_stage,  # increment as tour progresses
        "capacity": capacity,  # starts at 50 million
        "max_riders": max_riders,  # limitation of riders
    }

    df_riders = pd.read_excel(os.path.join(read_path, "riders_budget.xlsx"))

    df_riders = df_riders.dropna(subset=["price"])

    mip_optimize(df_riders, params, outputpath=read_path)


if __name__ == "__main__":
    main(
        starting_stage=5,
    )
