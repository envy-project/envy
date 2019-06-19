import json
import os
import shutil


class EnvyState:
    """ Manages ENVy's state through some files in the project's root directory
        Currently tracking:
            Environment hash: a hash of ENVy's environment config
            Container ID: the current ENVy environment container
            Image ID: the current ENVy environment image
    """

    def __init__(self, dir_path):
        self.directory = dir_path
        self.state = None

    def nuke(self):
        """ Removes the state directory
        """
        shutil.rmtree(self.directory)

    def get_image_hash(self) -> str:
        return self.__get(["image", "md5"])

    def set_image_hash(self, new_hash):
        self.__set(["image", "md5"], new_hash)

    def get_container_hash(self) -> str:
        return self.__get(["container", "md5"])

    def set_container_hash(self, new_hash):
        self.__set(["container", "md5"], new_hash)

    def get_container_id(self):
        return self.__get(["container", "dockerid"])

    def set_container_id(self, new_id):
        self.__set(["container", "dockerid"], new_id)

    def get_image_id(self):
        return self.__get(["image", "dockerid"])

    def set_image_id(self, new_id):
        self.__set(["image", "dockerid"], new_id)

    def __set(self, keys, value):
        state = self.__get_state()

        final_key = keys.pop()
        final_dict = state
        for key in keys:
            if not key in final_dict:
                final_dict[key] = {}
            final_dict = final_dict[key]

        final_dict[final_key] = value

        self.__set_state(state)

    def __get(self, keys):
        state = self.__get_state()

        final_key = keys.pop()
        final_dict = state
        for key in keys:
            if not key in final_dict:
                return None
            final_dict = final_dict[key]

        return final_dict.get(final_key, None)

    def __set_state(self, new_state):
        path = self.__get_state_path()

        with open(path, "w") as f:
            json.dump(new_state, f)

        self.state = new_state

    def __get_state(self) -> dict:
        if self.state is None:
            self.state = self.__load_state()

        return self.state

    def __load_state(self) -> dict:
        path = self.__get_state_path()

        if not os.path.isfile(path):
            return {}

        with open(path, "r") as f:
            return json.load(f)

    def __get_state_path(self):
        return "{}/state.json".format(self.directory)
