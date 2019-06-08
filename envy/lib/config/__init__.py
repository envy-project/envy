import sys

from .file import findConfigFile, parseConfigFile
from .validate import validateConfigFile

CONFIG_FILE_PATH = findConfigFile()
if CONFIG_FILE_PATH is None:
    sys.stderr.write("Envy config file not found.\n")
    sys.exit(1)
CONFIG_DATA = validateConfigFile(parseConfigFile(CONFIG_FILE_PATH))
