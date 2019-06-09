import os

from .directory import createDirectoryIfNotExists, ENVY_STATE_PATH
from .envy_state import EnvyState

createDirectoryIfNotExists()

ENVY_STATE = EnvyState(ENVY_STATE_PATH)
