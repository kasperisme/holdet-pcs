import numpy as np
from scipy import optimize
import pandas as pd
import json

df_riders = pd.read_excel("output/riders_budget.xlsx")


starting_stage = 0
capacity = 50000000  # 50 million
max_riders = 8

sizes = df_riders["price"].values
values = (
    df_riders[f"{starting_stage}_potential"].values
    + df_riders[f"{starting_stage+1}_potential"].values * 0.5
    + df_riders[f"{starting_stage+2}_potential"].values * 0.25
    + df_riders[f"{starting_stage+3}_potential"].values * 0.125
    + df_riders[f"{starting_stage+4}_potential"].values * 0.0625
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


df_riders["selected"] = res.x

print(
    df_riders[df_riders["selected"] == 1][
        ["name", "selected", "price", "teams_history"]
    ]
)

print("Total cost:", df_riders[df_riders["selected"] == 1]["price"].sum())
