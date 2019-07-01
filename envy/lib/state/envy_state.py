import json
import os
import shutil


class EnvyState:
    """ Manages ENVy's state through some files in the project's root directory
        Currently tracking:
            Environment hash: a hash of ENVy's environment config
            Container ID: the current ENVy environment container
    """

    def __init__(self, dir_path):
        self.directory = dir_path
        self.state = None

    def nuke(self):
        """ Removes the state directory
        """
        shutil.rmtree(self.directory)

    def get_container_id(self) -> str:
        return self.__get(["container", "dockerid"])

    def set_container_id(self, new_id: str):
        self.__set(["container", "dockerid"], new_id)

    def get_installed_packages(self):
        return self.__get(["packages"])

    def set_installed_packages(self, packages: [{}]):
        self.__set(["packages"], packages)

    def get_run_steps(self):
        return self.__get(["run_steps"]) or []

    def add_run_step(self, name):
        steps = self.get_run_steps()
        if name not in steps:
            steps.append(name)
            self.__set(["run_steps"], steps)

    def get_watchfile_hash(self, file: str) -> str:
        return self.__get(["watchfile", file])

    def set_watchfile_hash(self, file: str, new_hash: str):
        self.__set(["watchfile", file], new_hash)

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
