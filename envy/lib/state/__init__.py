import os

from .directory import create_directory_if_not_exists, ENVY_STATE_PATH
from .envy_state import EnvyState

create_directory_if_not_exists()

ENVY_STATE = EnvyState(ENVY_STATE_PATH)
