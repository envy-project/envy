import pathlib

_CONFIG_FILE_NAME = ".envyfile"


def findConfigFile():
    currentPath = pathlib.Path.cwd()
    while True:
        configPath = currentPath / _CONFIG_FILE_NAME
        if configPath.exists() and configPath.is_file():
            return configPath
        if currentPath == currentPath.parent:
            break
        currentPath = currentPath.parent
