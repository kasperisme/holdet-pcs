from src import stages, riders
import pandas as pd
from sklearn.preprocessing import StandardScaler
import os


def stage_loader(race: str, numberofstages: int, outputpath: str = "output"):
    stage_ls = stages.get_stages_dict(race, numberofstages)

    df_stage = pd.DataFrame(stage_ls)

    df_stage.to_excel(os.path.join(outputpath, "stages.xlsx"))

    return df_stage


def rider_loader(race: str, outputpath: str = "output"):
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

    df_riders.to_excel(os.path.join(outputpath, "riders.xlsx"))

    return df_riders


def potential(df_riders: pd.DataFrame, stage: pd.Series):
    profile = stage["profile"]

    profileindex = profile.split("-")[0].strip()

    if profileindex == "p1":
        return (
            (df_riders["one_day_races"] * 0)
            + (df_riders["gc"] * 2)
            + (df_riders["time_trial"] * 3)
            + (df_riders["sprint"] * 4)
            + (df_riders["climber"] * 1)
        )
    elif profileindex == "p2" or profileindex == "p4":
        return (
            (df_riders["one_day_races"] * 0)
            + (df_riders["gc"] * 2)
            + (df_riders["time_trial"] * 1)
            + (df_riders["sprint"] * 3)
            + (df_riders["climber"] * 4)
        )
    elif profileindex == "p3" or profileindex == "p5":
        return (
            (df_riders["one_day_races"] * 0)
            + (df_riders["gc"] * 3)
            + (df_riders["time_trial"] * 1)
            + (df_riders["sprint"] * 2)
            + (df_riders["climber"] * 4)
        )
    return 0


def analysis(
    df_riders: pd.DataFrame, df_stage: pd.DataFrame, outputpath: str = "output"
):
    scaler = StandardScaler()

    cols = ["one_day_races", "gc", "time_trial", "sprint", "climber"]

    df_riders[cols] = scaler.fit_transform(df_riders[cols].to_numpy())

    for index, stage in df_stage.iterrows():
        df_riders[str(index) + "_potential"] = potential(df_riders, stage)

    df_riders.to_excel(os.path.join(outputpath, "riders_stagepotential_analysis.xlsx"))

    return df_riders


def main(
    race: str = "race/tour-de-france/2024",
    numberofstages: int = 21,
    outputpath: str = "output",
):
    race = race
    numberofstages = numberofstages

    df_stages = stage_loader(race, numberofstages, outputpath)
    df_riders = rider_loader(race, outputpath)

    df_riders_potential = analysis(df_riders, df_stages, outputpath)


if __name__ == "__main__":
    main()
