from collections import OrderedDict

from envy.lib.docker_manager import ContainerManager
from envy.lib.config import ENVY_CONFIG

import envy.lib.triggers as triggers

from .script_setup_step import ScriptSetupStep
from .remote_setup_step import RemoteSetupStep


class Builder:
    """ Runs triggered build steps on a container
    """

    def __init__(self, container: ContainerManager):
        self.container = container
        self.steps = OrderedDict()

    def build(self):
        # Create system packages step
        self.__create_system_packages_step()

        # Create steps
        self.__create_steps()

        # Run triggered steps
        self.__run_triggered()

        # Persist triggers
        self.__persist_triggers()

    def __create_system_packages_step(self):
        pass

    def __create_steps(self):
        for m in ENVY_CONFIG.get_setup_steps():
            # Create step
            name = m["name"]
            if m["type"] == "script":
                step = ScriptSetupStep(name, self.container, m["run"])
            elif m["type"] == "remote":
                step = RemoteSetupStep(name, self.container, m["url"])

            # Create and register triggers
            if m["triggers"] == "once":
                trigger = triggers.TriggerOnce(name)
            elif m["triggers"] == "always":
                trigger = triggers.TriggerAlways()
            else:
                trigger_list = []
                for t in m["triggers"]["system-packages"]:
                    # TODO: swap this out once system packages aren't implemented in the image
                    trigger_list.append(triggers.TriggerPerContainer())
                    # trigger_list.append(triggers.TriggerSystemPackage(t))
                for t in m["triggers"]["files"]:
                    trigger_list.append(triggers.TriggerWatchfile(t))
                for t in m["triggers"]["steps"]:
                    trigger_list.append(triggers.TriggerStep(self.steps[t]))

                if trigger_list:
                    trigger = triggers.TriggerGroup(trigger_list)
                else:
                    trigger = triggers.TriggerPerContainer()

            step.set_trigger(trigger)

            # Add step to dict
            self.steps[name] = step

    def __run_triggered(self):
        for step in self.steps.values():
            if step.should_trigger():
                print("Running build step {}".format(step.name))
                step.run()
            else:
                print("Skipping build step {}".format(step.name))

    def __persist_triggers(self):
        for step in self.steps.values():
            if step.has_built():
                step.persist_trigger()
