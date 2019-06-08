import os

from envy.lib.config import hashEnvironmentConfig, ENVY_CONFIG

from .directory import ENVY_STATE_PATH

HASH_FILE_PATH = "{}/environment.md5".format(ENVY_STATE_PATH)


def didEnvironmentChange():
    return hashEnvironmentConfig(ENVY_CONFIG) != getHash()


def getHash():
    if os.path.isfile(HASH_FILE_PATH):
        with open(HASH_FILE_PATH, "r") as f:
            return f.read().rstrip()
    else:
        return None


def setHash(newHash):
    with open(HASH_FILE_PATH, "w") as f:
        f.write(newHash)
