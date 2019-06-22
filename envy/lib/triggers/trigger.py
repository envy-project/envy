from abc import ABC, abstractmethod


class Trigger(ABC):
    @abstractmethod
    def should_trigger(self) -> bool:
        """ Returns the value of this trigger. True if it has triggered.

        Returns:
            bool -- The result.
        """

    @abstractmethod
    def persist_trigger(self):
        """ Performs any actions required by this trigger when the associated build step has been run.
        """
