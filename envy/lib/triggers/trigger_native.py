from envy.lib.state import ENVY_STATE

from .trigger import Trigger


class TriggerNative(Trigger):
    """ Triggers whenever the given native dependency is reinstalled.
        NOTE: Currently we don't reinstall native dependencies piecemeal, so this triggers whenever the image is rebuilt.
    """

    def __init__(self, recipe: str):
        self.recipe = recipe

    def should_trigger(self) -> bool:
        # For now, we don't reinstall native dependencies piecemeal, so this check is sufficient.
        if ENVY_STATE.get_image_hash() is None:
            return True
        return False

    def persist_trigger(self):
        pass
