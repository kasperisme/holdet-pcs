from procyclingstats import Rider, RaceStartlist


def get_rider_stats(rider_id: str):
    return Rider(rider_id).parse()


def get_riders_dict(race: str):

    race_startlist = RaceStartlist(race + "/startlist")

    startlist_dict = race_startlist.parse()

    riders = []
    for i in startlist_dict["startlist"]:
        riders.append(get_rider_stats(i["rider_url"]))

    return riders
