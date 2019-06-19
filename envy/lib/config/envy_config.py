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

    def get_base_image(self) -> str:
        return self.data["environment"]["base"]["image"]

    def get_package_manager(self) -> str:
        config_manager = self.data["environment"]["base"]["package-manager"]

        if not config_manager:
            config_manager = self.__guess_package_manager()

        return config_manager

    def __guess_package_manager(self) -> str:
        return "apt"

    def get_native_dependencies(self) -> [{}]:
        return self.data["environment"]["native"]

    def get_actions(self) -> [{}]:
        return self.data.get("actions", [])

    def get_extra_executables(self) -> [{}]:
        return []  # TODO delete this

    def get_services_compose_path(self) -> Optional[str]:
        return self.data.get("services", {}).get("compose-file")
