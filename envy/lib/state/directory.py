from pathlib import Path
import os

from envy.lib.config import ENVY_PROJECT_DIR

_STATE_DIRECTORY = ".envy"

ENVY_STATE_PATH = "{}/{}".format(ENVY_PROJECT_DIR, _STATE_DIRECTORY)


def create_directory_if_not_exists():
    """ Creates the state directory if not found
    """
    if not os.path.isdir(ENVY_STATE_PATH):
        os.mkdir(ENVY_STATE_PATH)
        Path("{}/DO_NOT_COMMIT".format(ENVY_STATE_PATH)).touch()
