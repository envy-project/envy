import subprocess
from subprocess import DEVNULL


class ComposeManager:
    """ Manages a docker-compose file. Currently used for running sidecar services.
    """

    def __init__(self, compose_file: str):
        self.compose_file = compose_file

    # TODO compose may not be installed, should curl for it
    # TODO check subprocess outputs for error
    # TODO store created containers in state to avoid possible danglers
    # TODO I don't think we can do anything about this, but we *will* leave images dangling here. Probably just something we're ok with.

    def up(self):
        # TODO detect that pull is necessary and print something, since it can take a while
        subprocess.check_output(['docker-compose', '-f', self.compose_file, 'pull'], stderr=DEVNULL)
        subprocess.check_output(['docker-compose', '-f', self.compose_file, 'up', '-d'], stderr=DEVNULL)

    def down(self):
        subprocess.check_output(['docker-compose', '-f', self.compose_file, 'down'], stderr=DEVNULL)

    def nuke(self):
        subprocess.check_output(['docker-compose', '-f', self.compose_file, 'kill'], stderr=DEVNULL)
        subprocess.check_output(['docker-compose', '-f', self.compose_file, 'rm'], stderr=DEVNULL)
