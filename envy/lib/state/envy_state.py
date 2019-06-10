import os
import shutil

from envy.lib.config import ENVY_CONFIG


class EnvyState:
    """ Manages ENVy's state through some files in the project's root directory
        Currently tracking:
            Environment hash: a hash of ENVy's environment config
            Container ID: the current ENVy environment container
            Image ID: the current ENVy environment image
    """

    def __init__(self, dir_path):
        self.directory = dir_path

    def nuke(self):
        """ Removes the state directory
        """
        shutil.rmtree(self.directory)

    def did_environment_change(self) -> bool:
        """ Compares the state's environment hash against the current config's environment hash.
            Returns True if they don't match.

        Returns:
            bool -- The result
        """
        if self.get_environment_hash() is None:
            return False
        return ENVY_CONFIG.get_environment_hash() != self.get_environment_hash()

    def get_environment_hash(self) -> str:
        path = self.__get_environment_file()

        if os.path.isfile(path):
            with open(path, "r") as f:
                return f.read().rstrip()
        else:
            return None

    def set_environment_hash(self, new_hash):
        path = self.__get_environment_file()

        with open(path, "w") as f:
            f.write(new_hash)

    def update_environment_hash(self):
        self.set_environment_hash(ENVY_CONFIG.get_environment_hash())

    def __get_environment_file(self):
        return "{}/environment.md5".format(self.directory)

    def get_container_id(self):
        path = self.__get_container_file()

        if os.path.isfile(path):
            with open(path, "r") as f:
                return f.read().rstrip()
        else:
            return None

    def set_container_id(self, new_id):
        path = self.__get_container_file()

        with open(path, "w") as f:
            f.write(new_id)

    def __get_container_file(self):
        return "{}/container.dockerid".format(self.directory)

    def get_image_id(self):
        path = self.__get_image_file()

        if os.path.isfile(path):
            with open(path, "r") as f:
                return f.read().rstrip()
        else:
            return None

    def set_image_id(self, new_id):
        path = self.__get_image_file()

        with open(path, "w") as f:
            f.write(new_id)

    def __get_image_file(self):
        return "{}/image.dockerid".format(self.directory)
