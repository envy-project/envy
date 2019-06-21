from envy.lib.config import ENVY_CONFIG
from envy.lib.state import ENVY_STATE

from .trigger import Trigger


class TriggerPerContainer(Trigger):
    """ Triggers once per container
    """

    def should_trigger(self) -> bool:
        return ENVY_CONFIG.get_container_hash() != ENVY_STATE.get_container_hash()

    def persist_trigger(self):
        pass
