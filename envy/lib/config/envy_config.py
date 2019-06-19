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
        return (
            self.data.get("environment", {}).get("dependencies", {}).get("native", [])
        )

    def get_actions(self) -> [{}]:
        return self.data.get("actions", [])

    def get_extra_executables(self) -> [{}]:
        return (
            self.data.get("environment", {})
            .get("dependencies", {})
            .get("executables", [])
        )

    def get_services_compose_path(self) -> Optional[str]:
        return self.data.get("services", {}).get("compose-file")
