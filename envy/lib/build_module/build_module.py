from abc import ABC, abstractmethod

from envy.lib.docker_manager import ContainerManager


class BuildModule(ABC):
    """ A Build Module is a build step for an ENVy environment image.
        Build modules have a trigger, which tells the builder when they need to be run.

    See Also: trigger.py
    """

    def __init__(self, name: str, container: ContainerManager):
        self._name = name
        self._container = container
        self._has_run = False

    @property
    def name(self):
        return self._name

    @abstractmethod
    def run(self):
        """ Run this build module.
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
        """ Returns true if this build module has build within this ENVy run.

        Returns:
            bool -- The result
        """
        return self._has_run
