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
        relevant_dict = {
            "base": self.data["environment"]["base"],
            "system-packages": self.data["environment"]["system-packages"],
        }

        return hashlib.md5(
            json.dumps(relevant_dict, sort_keys=True).encode("utf-8")
        ).hexdigest()

    def get_container_hash(self) -> str:
        relevant_dict = {
            "steup-steps": self.data["environment"]["setup-steps"],
            "project-dir": self.data["environment"]["project-dir"],
        }

        return hashlib.md5(
            json.dumps(relevant_dict, sort_keys=True).encode("utf-8")
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

    def get_project_mount_path(self) -> str:
        path = self.data["environment"]["project-dir"]

        if path[-1] == "/":
            return path[: len(path) - 1]

        return path

    def get_system_packages(self) -> [{}]:
        return self.data["environment"]["system-packages"]

    def get_setup_steps(self) -> [{}]:
        return self.data["environment"]["setup-steps"]

    def get_actions(self) -> [{}]:
        return self.data["actions"]

    def get_services_compose_path(self) -> Optional[str]:
        return self.data["services"].get("compose-file")
