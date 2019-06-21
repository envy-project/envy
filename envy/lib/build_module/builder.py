from collections import OrderedDict

from envy.lib.docker_manager import ContainerManager
from envy.lib.config import ENVY_CONFIG

import envy.lib.triggers as triggers

from .script_build_module import ScriptBuildModule
from .remote_build_module import RemoteBuildModule


class Builder:
    """ Runs triggered build modules on a container
    """

    def __init__(self, container: ContainerManager):
        self.container = container
        self.modules = OrderedDict()

    def build(self):
        # Create modules
        self.__create_modules()

        # Run triggered modules
        self.__run_triggered()

        # Persist triggers
        self.__persist_triggers()

    def __create_modules(self):
        for m in ENVY_CONFIG.get_build_modules():
            # Create module
            name = m["name"]
            if m["type"] == "script":
                module = ScriptBuildModule(name, self.container, m["steps"])
            elif m["type"] == "remote":
                module = RemoteBuildModule(name, self.container, m["url"])

            # Create and register triggers
            if m["triggers"] == "once":
                trigger = triggers.TriggerOnce(name)
            elif m["triggers"] == "always":
                trigger = triggers.TriggerAlways()
            else:
                trigger_list = []
                for t in m["triggers"]["native"]:
                    trigger_list.append(triggers.TriggerNative(t))
                for t in m["triggers"]["files"]:
                    trigger_list.append(triggers.TriggerWatchfile(t))
                for t in m["triggers"]["modules"]:
                    trigger_list.append(triggers.TriggerModule(self.modules[t]))

                trigger = triggers.TriggerGroup(trigger_list)

            module.set_trigger(trigger)

            # Add module to dict
            self.modules[name] = module

    def __run_triggered(self):
        for module in self.modules.values():
            if module.should_trigger():
                print("Running build module {}".format(module.name))
                module.run()
            else:
                print("Skipping build module {}".format(module.name))

    def __persist_triggers(self):
        for module in self.modules.values():
            if module.has_built():
                module.persist_trigger()
