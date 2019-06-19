import subprocess
from subprocess import CalledProcessError


class ComposeManager:
    """ Manages a docker-compose file. Currently used for running sidecar services.
    """

    def __init__(self, compose_file: str):
        self.compose_file = compose_file

    # TODO compose may not be installed
    # TODO I don't think we can do anything about this, but we *will* leave images dangling here. Probably just something we're ok with.

    def up(self):
        # TODO detect that pull is necessary and print something, since it can take a while
        try:
            subprocess.run(
                ["docker-compose", "-f", self.compose_file, "pull"],
                check=True,
                capture_output=True,
            )
            subprocess.run(
                ["docker-compose", "-f", self.compose_file, "up", "-d"],
                check=True,
                capture_output=True,
            )
        except CalledProcessError as e:
            print(
                "Failed to start sidecar services. Command returned with error code {}".format(
                    e.returncode
                )
            )
            print(e.stdout.decode())
            print(e.stderr.decode())

    def down(self):
        try:
            subprocess.run(
                ["docker-compose", "-f", self.compose_file, "stop"],
                check=True,
                capture_output=True,
            )
        except CalledProcessError as e:
            print(
                "Failed to stop sidecar services. Command returned with error code {}".format(
                    e.returncode
                )
            )
            print(e.stdout.decode())
            print(e.stderr.decode())

    def nuke(self):
        try:
            subprocess.run(
                ["docker-compose", "-f", self.compose_file, "kill"],
                check=True,
                capture_output=True,
            )
            subprocess.run(
                ["docker-compose", "-f", self.compose_file, "rm", "-sf"],
                check=True,
                capture_output=True,
            )
        except CalledProcessError as e:
            print(
                "Failed to nuke sidecar services. Command returned with error code {}".format(
                    e.returncode
                )
            )
            print(e.stdout.decode())
            print(e.stderr.decode())
