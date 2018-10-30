import json
from pathlib import PurePath

from project.constants import PATH_PROJECT


def get_volume()->float:
    """
    Returns the volume value from the data.json file.
    Output ready for pygame.Sound.set_volume function.
    """
    with open(str(PurePath(PATH_PROJECT).joinpath("data.json"))) as f:
        data = json.load(f)

    if data["mute"]:
        return 0
    return data["volume"] / 100
