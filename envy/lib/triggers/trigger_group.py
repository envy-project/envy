from .trigger import Trigger


class TriggerGroup(Trigger):
    """ A group of triggers. Will trigger if any of its children have triggered.
    """

    def __init__(self, children: [Trigger]):
        self.children = children

    def should_trigger(self) -> bool:
        result = False
        for child in self.children:
            result = result or child.should_trigger()

        return result

    def persist_trigger(self):
        for child in self.children:
            child.persist_trigger()
