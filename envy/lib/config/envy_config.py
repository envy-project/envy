import hashlib
import json
import yaml

from .schema import validateSchema


class EnvyConfig:
    def __init__(self, filePath):
        self.file = filePath

        with filePath.open() as f:
            raw_data = yaml.safe_load(f)

        self.data = validateSchema(raw_data)

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
