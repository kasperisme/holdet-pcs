from procyclingstats import Stage

profile_trans_dict = {
    "p1": "Flat",
    "p2": "Hills, flat finish",
    "p3": "Hills, uphill finish",
    "p4": "Mountains, flat finish",
    "p5": "Mountains, uphill finish",
}


def get_stages_dict(race: str, numberofstages: int):
    stage_lst = []
    for i in range(1, 1 + numberofstages):
        stage = Stage(race + "/stage-" + str(i))

        stage_dict = {}

        stage_dict["number"] = i
        stage_dict["date"] = stage.date()
        stage_dict["departure"] = stage.departure()
        stage_dict["arrival"] = stage.arrival()
        stage_dict["distance"] = stage.distance()
        stage_dict["type"] = stage.stage_type()
        stage_dict["vertical"] = stage.vertical_meters()
        stage_dict["profile"] = (
            stage.profile_icon() + " -  " + profile_trans_dict[stage.profile_icon()]
        )
        stage_dict["race_startlist_quality_score"] = (
            stage.race_startlist_quality_score()
        )
        stage_dict["profile_score"] = stage.profile_score()

        stage_lst.append(stage_dict)

    return stage_lst
