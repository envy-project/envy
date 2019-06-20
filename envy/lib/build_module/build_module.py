from abc import ABC, abstractmethod

from envy.lib.triggers import Trigger
from envy.lib.docker_manager import ContainerManager


class BuildModule(ABC):
    """ A Build Module is a non-native build step for an ENVy environment image.
        Build modules have a trigger, which tells the builder when they need to be run.

    See Also: trigger.py
    """

    def __init__(self, name: str, container: ContainerManager):
        self.name = name
        self.container = container
        self.has_run = False
        self.trigger = None

    @abstractmethod
    def run(self):
        """ Run this build module.
            Does NOT check the trigger! Run should_trigger() first if you care.
        """
        self.has_run = True

    def set_trigger(self, trigger: Trigger):
        """ Sets the trigger for this build module

        Arguments:
            trigger {Trigger} -- The trigger
        """
        self.trigger = trigger

    def should_trigger(self) -> bool:
        """ Returns true if a trigger is configured, and that trigger is triggered.

        Returns:
            bool -- The result
        """
        if self.trigger:
            return self.trigger.should_trigger()

        return False

    def persist_trigger(self):
        if self.trigger:
            self.trigger.persist_trigger()

    def has_built(self) -> bool:
        """ Returns true if this build module has build within this ENVy run.

        Returns:
            bool -- The result
        """
        return self.has_run
