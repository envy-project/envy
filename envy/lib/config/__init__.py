import sys

from .file import findConfigFile, parseConfigFile
from .validate import validateConfigFile

ENVY_CONFIG_FILE_PATH = findConfigFile()
if ENVY_CONFIG_FILE_PATH is None:
    sys.stderr.write("Envy config file not found.\n")
    sys.exit(1)
ENVY_CONFIG = validateConfigFile(parseConfigFile(ENVY_CONFIG_FILE_PATH))
