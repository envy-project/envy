import os
import shutil

from envy.lib.config import ENVY_CONFIG


class EnvyState:
    def __init__(self, dirPath):
        self.directory = dirPath

    def nuke(self):
        shutil.rmtree(self.directory)

    def did_environment_chane(self):
        if self.get_environment_hash() is None:
            return False
        return ENVY_CONFIG.get_environment_hash() != self.get_environment_hash()

    def get_environment_hash(self):
        path = self.get_environment_file()

        if os.path.isfile(path):
            with open(path, "r") as f:
                return f.read().rstrip()
        else:
            return None

    def set_environment_hash(self, new_hash):
        path = self.get_environment_file()

        with open(path, "w") as f:
            f.write(new_hash)

    def update_environment_hash(self):
        self.set_environment_hash(ENVY_CONFIG.get_environment_hash())

    def get_environment_file(self):
        return "{}/environment.md5".format(self.directory)

    def get_container_id(self):
        path = self.get_container_file()

        if os.path.isfile(path):
            with open(path, "r") as f:
                return f.read().rstrip()
        else:
            return None

    def set_container_id(self, new_id):
        path = self.get_container_file()

        with open(path, "w") as f:
            f.write(new_id)

    def get_container_file(self):
        return "{}/container.dockerid".format(self.directory)

    def get_image_id(self):
        path = self.get_image_file()

        if os.path.isfile(path):
            with open(path, "r") as f:
                return f.read().rstrip()
        else:
            return None

    def set_image_id(self, new_id):
        path = self.get_image_file()

        with open(path, "w") as f:
            f.write(new_id)

    def get_image_file(self):
        return "{}/image.dockerid".format(self.directory)
