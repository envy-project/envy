from .trigger import Trigger


class TriggerAlways(Trigger):
    """ A trigger that always triggers.
    """

    def __init__(self):
        pass

    def should_trigger(self) -> bool:
        return True

    def persist_trigger(self):
        pass
