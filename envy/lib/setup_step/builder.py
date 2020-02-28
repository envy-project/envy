import os
import pwd
import grp

from collections import OrderedDict

from envy.lib.docker_manager import ContainerManager
from envy.lib.io import StepPrinter
from envy.lib.config import ENVY_CONFIG

import envy.lib.triggers as triggers

from .script_setup_step import ScriptSetupStep
from .remote_setup_step import RemoteSetupStep
from .apt_package_manager_step import AptPackageManagerStep


class Builder:
    """ Runs triggered build steps on a container
    """

    def __init__(self, container: ContainerManager, printer: StepPrinter):
        self.container = container
        self.printer = printer
        self.steps = OrderedDict()
        self.system_package_step = None

    def build(self):
        # Create system packages step
        self.__create_system_packages_step()

        # Create initial-setup step
        self.__create_initial_setup_steps()

        # Create steps
        self.__create_steps()

        # Run triggered steps
        self.__run_triggered()

        # Persist triggers
        self.__persist_triggers()

    def __create_system_packages_step(self):
        self.system_package_step = AptPackageManagerStep(
            self.container, ENVY_CONFIG.get_system_packages()
        )
        self.steps[self.system_package_step.name] = self.system_package_step

    def __create_initial_setup_steps(self):
        # Set up this user's username and groups inside the container.
        uid = os.getuid()
        gid = os.getgid()
        groups = os.getgroups()
        uname = pwd.getpwuid(uid).pw_name

        group_info = [grp.getgrgid(group) for group in groups]
        group_creation = [
            "echo '{}:x:{}:{}' >> /etc/group".format(
                group.gr_name, str(group.gr_gid), uname if group.gr_gid != gid else ""
            )
            for group in group_info
        ]

        chmod_step = ScriptSetupStep(
            "ENVY_chmod_root",
            "Setting up home environment",
            self.container,
            [
                "chmod a+wrx /root",
                "chmod a+wrx /",
                "echo '{}:x:{}:{}::/uhome:/bin/bash' >> /etc/passwd".format(
                    uname, str(uid), str(gid)
                ),
                "mkdir /uhome",
                "chown {}:{} /uhome".format(str(uid), str(gid)),
            ]
            + group_creation,
            False,
        )
        self.steps[chmod_step.name] = chmod_step

    def __create_steps(self):
        for m in ENVY_CONFIG.get_setup_steps():
            # Create step
            name = m["name"]
            label = m["label"]
            if m["type"] == "script":
                step = ScriptSetupStep(
                    name, label, self.container, m["run"], m["as_user"]
                )
            elif m["type"] == "remote":
                step = RemoteSetupStep(name, label, self.container, m["url"])

            # Create and register triggers
            if m["triggers"] == "always":
                trigger = triggers.TriggerAlways()
            else:
                trigger_list = []
                for t in m["triggers"]["system-packages"]:
                    trigger_list.append(
                        triggers.TriggerSystemPackage(t, self.system_package_step)
                    )
                for t in m["triggers"]["files"]:
                    trigger_list.append(triggers.TriggerWatchfile(t))
                for t in m["triggers"]["steps"]:
                    trigger_list.append(triggers.TriggerStep(self.steps[t]))

                trigger = triggers.TriggerGroup(trigger_list)

            step.set_trigger(trigger)

            # Add step to dict
            self.steps[name] = step

    def __run_triggered(self):
        for step in self.steps.values():
            if step.should_trigger():
                self.printer.start_step(step.label)
                step.run()
                self.printer.end_step()
            else:
                self.printer.skip_step(step.label)

    def __persist_triggers(self):
        for step in self.steps.values():
            if step.has_built():
                step.persist_trigger()
