import hashlib
import json
import pathlib
import sys
import yaml

from schema import Schema, SchemaError, Optional, Or

_CONFIG_FILE_NAME = ".envyfile"

# TODO add schema information for environment stuff
_SCHEMA = Schema(
    {
        Optional("environment", default={}): {
            Optional("dependencies", default={}): {
                Optional("python2", default="requirements.txt"): str,
                Optional("python3", default="Pipfile"): str,
                Optional("node", default="package.json"): str,
                Optional("ruby", default="gemfile"): str,
                Optional("native", default=[]): [
                    {"recipe": str, "version": Or(str, int, float)}
                ],
            }
        },
        Optional("actions"): [
            {"name": str, "script": str, "help": str, Optional("description"): str}
        ],
    }
)


def findConfigFile():
    currentPath = pathlib.Path.cwd()
    while True:
        configPath = currentPath / _CONFIG_FILE_NAME
        if configPath.exists() and configPath.is_file():
            return configPath
        if currentPath == currentPath.parent:
            break
        currentPath = currentPath.parent


class EnvyConfig:
    def __init__(self, filePath):
        self.file = filePath

        with filePath.open() as f:
            raw_data = yaml.safe_load(f)

        try:
            self.data = _SCHEMA.validate(raw_data)
        except SchemaError as e:
            sys.exit(e.code)

    def getEnvironmentHash(self):
        return hashlib.md5(
            json.dumps(self.data["environment"]).encode("utf-8")
        ).hexdigest()

    def getFullHash(self):
        return hashlib.md5(json.dumps(self.data).encode("utf-8")).hexdigest()

    def getNativeDependencies(self):
        return self.data["environment"]["dependencies"]["native"]

    def getActions(self):
        return self.data["actions"]

    def getExtraExecutables(self):
        return []  # TODO
