from source import stages, riders
import pandas as pd


race = "race/tour-de-france/2024"
numberofstages = 21


stage_ls = stages.get_stages_dict(race, numberofstages)

print(stage_ls)

df_stage = pd.DataFrame(stage_ls)

df_stage.to_excel("output/stages.xlsx")

riders_ls = riders.get_riders_dict(race)
df_riders = pd.DataFrame(riders_ls)

df_riders = pd.concat(
    [
        df_riders.drop(["points_per_speciality"], axis=1),
        df_riders["points_per_speciality"].apply(pd.Series),
    ],
    axis=1,
)

df_riders = pd.concat(
    [
        df_riders.drop(["points_per_season_history"], axis=1),
        df_riders["points_per_season_history"].apply(pd.Series),
    ],
    axis=1,
)


df_riders.to_excel("output/riders.xlsx")
