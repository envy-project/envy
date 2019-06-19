from pathlib import Path
from typing import Optional

import hashlib
import json
import yaml

from .schema import validate as validate_schema


class EnvyConfig:
    """ Reads the envyfile as specified in schema.py.
        Data is available in EnvyConfig.data, or with some accessors for important data.

    See Also: schema.py
    """

    def __init__(self, file_path: Path):
        self.file = file_path

        with file_path.open() as f:
            raw_data = yaml.safe_load(f)

        self.data = validate_schema(raw_data)

    def get_environment_hash(self) -> str:
        return hashlib.md5(
            json.dumps(self.data["environment"], sort_keys=True).encode("utf-8")
        ).hexdigest()

    def get_full_hash(self) -> str:
        return hashlib.md5(
            json.dumps(self.data, sort_keys=True).encode("utf-8")
        ).hexdigest()

    def get_native_dependencies(self) -> [{}]:
        if (
            "dependencies" in self.data["environment"]
            and "native" in self.data["environment"]["dependencies"]
        ):
            return self.data["environment"]["dependencies"]["native"]

        return []

    def get_actions(self) -> [{}]:
        return self.data["actions"]

    def get_extra_executables(self) -> [{}]:
        if (
            "dependencies" in self.data["environment"]
            and "executables" in self.data["environment"]["dependencies"]
        ):
            return self.data["environment"]["dependencies"]["executables"]

        return []

    def get_services_compose_path(self) -> Optional[str]:
        if "compose-file" in self.data["services"]:
            return self.data["services"]["compose-file"]

        return None
