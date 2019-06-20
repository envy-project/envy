import os
from pathlib import Path
from typing import Optional

from envy.lib.config import ENVY_PROJECT_DIR

from .trigger import Trigger


class TriggerOnce(Trigger):
    """ Triggers once, ever. Uses a file outside the .envy state directory to survive `envy nuke`.
        The filepath can be forced the optional force_path argument.
    """

    def __init__(self, name: str, force_path: Optional[str] = None):
        self.name = name
        self.path = force_path or self.__generate_path()

    def should_trigger(self) -> bool:
        return not os.path.isfile(self.path)

    def persist_trigger(self):
        Path(self.path).touch()

    def __generate_path(self):
        return "{}/.envy-trigger-{}".format(ENVY_PROJECT_DIR, self.name)
