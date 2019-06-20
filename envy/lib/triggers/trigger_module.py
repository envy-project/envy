from envy.lib.build_module.build_module import BuildModule

from .trigger import Trigger


class TriggerModule(Trigger):
    """ Triggers whenever the given module rebuilds.
    """

    def __init__(self, module: BuildModule):
        self.module = module

    def should_trigger(self) -> bool:
        return self.module.has_built()

    def persist_trigger(self):
        pass
