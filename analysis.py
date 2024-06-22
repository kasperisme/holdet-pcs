import pandas as pd


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
        df_riders[index + "_potential"] = (
            (df_riders["points_per_speciality"]["one_day_races"] * 4)
            + (df_riders["points_per_speciality"]["gc"] * 2)
            + (df_riders["points_per_speciality"]["time_trial"] * 3)
            + (df_riders["points_per_speciality"]["sprint"] * 5)
            + (df_riders["points_per_speciality"]["climber"] * 1)
        )
    elif profileindex == "p2":
        df_riders[index + "_potential"] = (
            (df_riders["points_per_speciality"]["one_day_races"] * 4)
            + (df_riders["points_per_speciality"]["gc"] * 2)
            + (df_riders["points_per_speciality"]["time_trial"] * 3)
            + (df_riders["points_per_speciality"]["sprint"] * 5)
            + (df_riders["points_per_speciality"]["climber"] * 1)
        )

    return 0


for index, stage in df_stage.iterrows():
    potential(stage, index)
