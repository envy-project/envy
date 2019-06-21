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

    def get_image_hash(self) -> str:
        return hashlib.md5(
            json.dumps(self.data["environment"]["base"], sort_keys=True).encode("utf-8")
        ).hexdigest()

    def get_container_hash(self) -> str:
        return hashlib.md5(
            json.dumps(
                self.data["environment"]["build-modules"], sort_keys=True
            ).encode("utf-8")
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

    def get_build_modules(self) -> [{}]:
        return self.data["environment"]["build-modules"]

    def get_actions(self) -> [{}]:
        return self.data["actions"]

    def get_services_compose_path(self) -> Optional[str]:
        return self.data["services"].get("compose-file")
