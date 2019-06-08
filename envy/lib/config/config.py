import sys

from .envy_config import findConfigFile, EnvyConfig

ENVY_CONFIG_FILE_PATH = findConfigFile()
if ENVY_CONFIG_FILE_PATH is None:
    sys.stderr.write("Envy config file not found.\n")
    sys.exit(1)

ENVY_CONFIG = EnvyConfig(ENVY_CONFIG_FILE_PATH)
