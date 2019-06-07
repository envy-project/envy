import pathlib

import yaml

_CONFIG_FILE_NAME = ".envy-conf"


def findConfigFile():
    currentPath = pathlib.Path.cwd()
    while True:
        configPath = currentPath / _CONFIG_FILE_NAME
        if configPath.exists() and configPath.is_file():
            return configPath
        if currentPath == currentPath.parent:
            break
        currentPath = currentPath.parent


def parseConfigFile(filePath):
    with filePath.open() as f:
        return yaml.safe_load(f)
