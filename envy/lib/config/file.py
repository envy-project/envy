import pathlib

_CONFIG_FILE_NAME = ".envyfile"


def find_config_file():
    current_path = pathlib.Path.cwd()
    while True:
        config_path = current_path / _CONFIG_FILE_NAME
        if config_path.exists() and config_path.is_file():
            return config_path
        if current_path == current_path.parent:
            break
        current_path = current_path.parent
