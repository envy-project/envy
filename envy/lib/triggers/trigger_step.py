from envy.lib.setup_step.setup_step import SetupStep

from .trigger import Trigger


class TriggerStep(Trigger):
    """ Triggers whenever the given step rebuilds.
    """

    def __init__(self, step: SetupStep):
        self.step = step

    def should_trigger(self) -> bool:
        return self.step.has_built()

    def persist_trigger(self):
        pass
