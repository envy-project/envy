import hashlib
import os

from envy.lib.state import ENVY_STATE

from .trigger import Trigger

CHUNK_SIZE = 4096


class TriggerWatchfile(Trigger):
    """ Triggers whenever the given file changes.
        Stores a hash of the file's contents in the state to determine changes.
    """

    def __init__(self, watchfile: str):
        self.watchfile = watchfile
        self.name_hash = self.__compute_name_hash()
        self.file_hash = self.__compute_file_hash()

    def should_trigger(self) -> bool:
        return ENVY_STATE.get_watchfile_hash(self.name_hash) != self.file_hash

    def persist_trigger(self):
        ENVY_STATE.set_watchfile_hash(self.name_hash, self.file_hash)

    def __compute_file_hash(self):
        md5 = hashlib.md5()

        if os.path.isfile(self.watchfile):
            with open(self.watchfile, "rb") as f:
                for chunk in iter(lambda: f.read(CHUNK_SIZE), b""):
                    md5.update(chunk)

        return md5.hexdigest()

    def __compute_name_hash(self):
        return hashlib.md5(self.watchfile.encode()).hexdigest()
