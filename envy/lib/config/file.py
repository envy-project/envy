from pathlib import Path

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


def find_relative_cwd() -> Path:
    """ Finds the relative current working directory based on the root of the ENVy project.
        Does not return a Path as the result is *not* a useful path object.

    Returns:
        [Path] -- relative path to cwd from project root
    """
    cwd = Path.cwd()
    return cwd.relative_to(find_config_file().parent)
