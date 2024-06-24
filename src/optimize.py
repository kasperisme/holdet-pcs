import numpy as np
from scipy import optimize
import pandas as pd
import os


def mip_optimize(df_riders: pd.DataFrame, params: dict):
    starting_stage = params["starting_stage"]
    capacity = params["capacity"]
    max_riders = params["max_riders"]
    depreciation_factor = params["depreciation_factor"]

    sizes = df_riders["price"].values
    values = (
        df_riders[f"{starting_stage}_potential"].values
        + df_riders[f"{starting_stage+1}_potential"].values * (depreciation_factor**1)
        + df_riders[f"{starting_stage+2}_potential"].values * (depreciation_factor**2)
        + df_riders[f"{starting_stage+3}_potential"].values * (depreciation_factor**3)
        + df_riders[f"{starting_stage+4}_potential"].values * (depreciation_factor**4)
    )

    bounds = optimize.Bounds(0, 1)  # 0 <= x_i <= 1
    integrality = np.full_like(values, True)  # x_i are integers
    capactiy_constraint = optimize.LinearConstraint(A=sizes, lb=0, ub=capacity)

    max_riders_constraint = optimize.LinearConstraint(
        A=np.ones_like(sizes), lb=0, ub=max_riders
    )

    constraints = [capactiy_constraint, max_riders_constraint]

    res = optimize.milp(
        c=-values, constraints=constraints, integrality=integrality, bounds=bounds
    )

    df_riders["team"] = df_riders["teams_history"].apply(
        lambda x: x[x.find("'season': 2024") + 30 :][: x.find("'season': 2023")]
    )

    df_riders["selected"] = res.x

    print(
        df_riders[df_riders["selected"] == 1][
            ["name", "price", f"{starting_stage}_potential", "team"]
        ]
    )

    print("Total cost:", df_riders[df_riders["selected"] == 1]["price"].sum())


def main(
    starting_stage: int = 0,
    capacity: int = 50000000,
    max_riders: int = 8,
    depreciation_factor: float = 0.5,
    read_path: str = "output",
):
    params = {
        "starting_stage": starting_stage,  # increment as tour progresses
        "capacity": capacity,  # starts at 50 million
        "max_riders": max_riders,  # limitation of riders
        "depreciation_factor": depreciation_factor,  # depreciation for each stage, the higher the factor the more important is the next stages
    }

    df_riders = pd.read_excel(os.path.join(read_path, "riders_budget.xlsx"))

    df_riders = df_riders.dropna(subset=["price"])

    mip_optimize(df_riders, params)


if __name__ == "__main__":
    main()
