from pathlib import Path
import os

_CONFIG_FILE_NAME = ".envyfile"


def find_config_file() -> Path:
    """ Finds the envyfile by traversing upwards from the cwd until a file matching _CONFIG_FILE_NAME is found

    Returns:
        [Path] -- Path to the envyfile
    """
    current_path = Path.cwd()
    while True:
        config_path = current_path / _CONFIG_FILE_NAME
        if config_path.exists() and config_path.is_file():
            return config_path
        if current_path == current_path.parent:
            break
        current_path = current_path.parent


def findProjectRoot() -> str:
    """ Finds the project root as defined by ENVy:
        the folder that contains the Envyfile
        Returns:
            [str] -- Absolute path to the root of the project.
    """
    return os.path.dirname(findConfigFile())
