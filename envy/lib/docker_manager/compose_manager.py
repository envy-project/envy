import subprocess

class ComposeManager:
    """ Manages a docker-compose file. Currently used for running sidecar services.
    """

    def __init__(self, compose_file: str):
        self.compose_file = compose_file

    # TODO check subprocess outputs for error
    # TODO store created containers in state to avoid possible danglers
    # TODO I don't think we can do anything about this, but we *will* leave images dangling here. Probably just something we're ok with.

    def up(self):
        subprocess.check_output("docker-compose pull -f {} -d".format(self.compose_file))
        subprocess.check_output("docker-compose up -f {} -d".format(self.compose_file))

    def down(self):
        subprocess.check_output("docker-compose down -f {}".format(self.compose_file))

    def nuke(self):
        subprocess.check_output("docker-compose kill -f {}".format(self.compose_file))
        subprocess.check_output("docker-compose rm -f {}".format(self.compose_file))
