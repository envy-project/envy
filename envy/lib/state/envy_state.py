import os

from envy.lib.config import ENVY_CONFIG


class EnvyState:
    def __init__(self, dirPath):
        self.directory = dirPath

    def didEnvironmentChange(self):
        return ENVY_CONFIG.getEnvironmentHash() != self.getEnvironmentHash()

    def getEnvironmentHash(self):
        path = self.getEnvironmentFile()

        if os.path.isfile(path):
            with open(path, "r") as f:
                return f.read().rstrip()
        else:
            return None

    def setEnvironmentHash(self, newHash):
        path = self.getEnvironmentFile()

        with open(path, "w") as f:
            f.write(newHash)

    def updateEnvironmentHash(self):
        self.setEnvironmentHash(ENVY_CONFIG.getEnvironmentHash())

    def getEnvironmentFile(self):
        return "{}/environment.md5".format(self.directory)

    def getContainerID(self):
        path = self.getContainerFile()

        if os.path.isfile(path):
            with open(path, "r") as f:
                return f.read().rstrip()
        else:
            return None

    def setContainerID(self, newID):
        path = self.getContainerFile()

        with open(path, "w") as f:
            f.write(newID)

    def getContainerFile(self):
        return "{}/container.dockerid".format(self.directory)
