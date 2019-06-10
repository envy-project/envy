import sys

from .file import find_config_file
from .envy_config import EnvyConfig

ENVY_CONFIG_FILE_PATH = find_config_file()
if ENVY_CONFIG_FILE_PATH is None:
    sys.stderr.write("Envy config file not found.\n")
    sys.exit(1)

ENVY_CONFIG = EnvyConfig(ENVY_CONFIG_FILE_PATH)
