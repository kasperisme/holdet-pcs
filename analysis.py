import pandas as pd
from sklearn.preprocessing import StandardScaler


df_riders = pd.read_excel("output/riders.xlsx")
df_stage = pd.read_excel("output/stages.xlsx")

"""
profile_trans_dict = {
    "p1": "Flat",
    "p2": "Hills, flat finish",
    "p3": "Hills, uphill finish",
    "p4": "Mountains, flat finish",
    "p5": "Mountains, uphill finish",
}


one_day_races	gc	time_trial	sprint	climber

"""


def potential(stage, index):
    profile = stage["profile"]

    profileindex = profile.split("-")[0].strip()

    if profileindex == "p1":
        df_riders[str(index) + "_potential"] = (
            (df_riders["one_day_races"] * 0)
            + (df_riders["gc"] * 2)
            + (df_riders["time_trial"] * 3)
            + (df_riders["sprint"] * 4)
            + (df_riders["climber"] * 1)
        )
    elif profileindex == "p2" or profileindex == "p4":
        df_riders[str(index) + "_potential"] = (
            (df_riders["one_day_races"] * 0)
            + (df_riders["gc"] * 2)
            + (df_riders["time_trial"] * 1)
            + (df_riders["sprint"] * 3)
            + (df_riders["climber"] * 4)
        )
    elif profileindex == "p3" or profileindex == "p5":
        df_riders[str(index) + "_potential"] = (
            (df_riders["one_day_races"] * 0)
            + (df_riders["gc"] * 3)
            + (df_riders["time_trial"] * 1)
            + (df_riders["sprint"] * 2)
            + (df_riders["climber"] * 4)
        )
    return 0


scaler = StandardScaler()

cols = ["one_day_races", "gc", "time_trial", "sprint", "climber"]

df_riders[cols] = scaler.fit_transform(df_riders[cols].to_numpy())


for index, stage in df_stage.iterrows():
    potential(stage, index)


df_riders.to_excel("output/riders_stagepotential_analysis.xlsx")
