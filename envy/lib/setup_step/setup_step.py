from abc import ABC, abstractmethod
from typing import Optional

from envy.lib.docker_manager import ContainerManager


class SetupStep(ABC):
    """ A Build Step is a build step for an ENVy environment image.
        Build steps have a trigger, which tells the builder when they need to be run.

    See Also: trigger.py
    """

    def __init__(self, name: str, label: Optional[str], container: ContainerManager):
        self._name = name
        self._label = label or name
        self._container = container
        self._has_run = False

    @property
    def name(self):
        return self._name

    @property
    def label(self):
        return self._label

    @abstractmethod
    def run(self):
        """ Run this build step.
            Does NOT check the trigger! Run should_trigger() first if you care.
        """
        self._has_run = True

    @abstractmethod
    def should_trigger(self) -> bool:
        """ Returns true if a trigger is configured, and that trigger is triggered.

        Returns:
            bool -- The result
        """
        raise NotImplementedError()

    @abstractmethod
    def persist_trigger(self):
        pass

    def has_built(self) -> bool:
        """ Returns true if this build step has build within this ENVy run.

        Returns:
            bool -- The result
        """
        return self._has_run
