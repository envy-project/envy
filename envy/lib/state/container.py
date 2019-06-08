import os

from .directory import ENVY_STATE_PATH

CONTAINER_FILE_PATH = "{}/envy_container".format(ENVY_STATE_PATH)


def getContainerID():
    if os.path.isfile(CONTAINER_FILE_PATH):
        with open(CONTAINER_FILE_PATH, "r") as f:
            return f.read().rstrip()
    else:
        return None


def setContainerID(newID):
    with open(CONTAINER_FILE_PATH, "w") as f:
        f.write(newID)
