import json
from pathlib import PurePath

from project.constants import PATH_PROJECT


def get_volume()->float:
    with open(str(PurePath(PATH_PROJECT).joinpath("data.json"))) as f:
        data = json.load(f)

    if data["mute"]:
        return 0
    else:
        return data["volume"] / 100
