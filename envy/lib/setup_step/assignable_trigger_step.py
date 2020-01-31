from abc import abstractmethod
from typing import Optional

from envy.lib.triggers import Trigger
from envy.lib.state import ENVY_STATE
from envy.lib.docker_manager import ContainerManager

from .setup_step import SetupStep


class AssignableTriggerStep(SetupStep):
    """ A Build Step that allows its trigger to be set
    """

    def __init__(self, name: str, label: Optional[str], container: ContainerManager):
        super(AssignableTriggerStep, self).__init__(name, label, container)
        self._trigger = None

    def set_trigger(self, trigger: Trigger):
        """ Sets the trigger for this build step

        Arguments:
            trigger {Trigger} -- The trigger
        """
        self._trigger = trigger

    def should_trigger(self) -> bool:
        """ Returns true if a trigger is configured, and that trigger is triggered.

        Returns:
            bool -- The result
        """
        if self.name not in ENVY_STATE.get_run_steps():
            return True

        if self._trigger:
            return self._trigger.should_trigger()

        return False

    def persist_trigger(self):
        ENVY_STATE.add_run_step(self.name)
        if self._trigger:
            self._trigger.persist_trigger()

    @abstractmethod
    def run(self):
        super().run()
