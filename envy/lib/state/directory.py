from pathlib import Path
import os

from envy.lib.config import ENVY_CONFIG_FILE_PATH

_STATE_DIRECTORY = ".envy"

ENVY_STATE_PATH = "{}/{}".format(
    os.path.dirname(ENVY_CONFIG_FILE_PATH), _STATE_DIRECTORY
)


def createDirectoryIfNotExists():
    if not os.path.isdir(ENVY_STATE_PATH):
        os.mkdir(ENVY_STATE_PATH)
        Path("{}/DO_NOT_COMMIT".format(ENVY_STATE_PATH)).touch()
