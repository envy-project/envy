import hashlib
import json
import yaml

from .schema import validate as validate_schema


class EnvyConfig:
    def __init__(self, file_path):
        self.file = file_path

        with file_path.open() as f:
            raw_data = yaml.safe_load(f)

        self.data = validate_schema(raw_data)

    def get_environment_hash(self):
        return hashlib.md5(
            json.dumps(self.data["environment"], sort_keys=True).encode("utf-8")
        ).hexdigest()

    def get_full_hash(self):
        return hashlib.md5(
            json.dumps(self.data, sort_keys=True).encode("utf-8")
        ).hexdigest()

    def get_native_dependencies(self):
        return self.data["environment"]["dependencies"]["native"]

    def get_actions(self):
        return self.data["actions"]

    def get_extra_executables(self):
        return self.data["environment"]["dependencies"]["executables"]
