import sys
import os

from .file import find_config_file, find_relative_cwd
from .envy_config import EnvyConfig

ENVY_CONFIG_FILE_PATH = find_config_file()
if ENVY_CONFIG_FILE_PATH is None:
    sys.stderr.write("Envy config file not found.\n")
    sys.exit(1)

ENVY_CURRENT_RELATIVE_PATH = find_relative_cwd()

ENVY_PROJECT_DIR = ENVY_CONFIG_FILE_PATH.parent

ENVY_CONFIG = EnvyConfig(ENVY_CONFIG_FILE_PATH)
