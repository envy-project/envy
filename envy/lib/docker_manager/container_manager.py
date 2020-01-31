from hashlib import md5
import os
from pathlib import Path
from docker.types import Mount
from docker import DockerClient
from docker.models.containers import Container
import dockerpty

from envy.lib.config import ENVY_PROJECT_DIR, ENVY_CONFIG


class ContainerNotFound(Exception):
    pass


class ContainerNotRunning(Exception):
    pass


class ContainerError(Exception):
    def __init__(self, code):
        super(ContainerError, self).__init__(code)
        self.code = code


class ContainerManager:
    ### Static Container Creation ###
    @staticmethod
    def __generate_container_name() -> str:
        return f"envy-{ENVY_PROJECT_DIR.name}-{md5(str(ENVY_PROJECT_DIR).encode()).hexdigest()}-container"

    @staticmethod
    def create(docker_client: DockerClient, image_id: str) -> "ContainerManager":
        """ Creates a container with the given image id

        Arguments:
            docker_client {DockerClient} -- A docker client
            image_id {str} -- the ID of the image to use

        Returns:
            ContainerManager -- a container manager for the created container
        """
        print("Creating ENVy container")

        container = docker_client.containers.create(
            image_id,
            "tail -f /dev/null",
            name=ContainerManager.__generate_container_name(),
            network_mode="host",
            mounts=[
                Mount(
                    ENVY_CONFIG.get_project_mount_path(),
                    str(ENVY_PROJECT_DIR),
                    type="bind",
                ),
                Mount("/var/run/docker.sock", "/var/run/docker.sock", type="bind"),
            ],
        )

        return ContainerManager(docker_client, container.id)

    ### Container Management ###
    def __init__(self, docker_client: DockerClient, container_id: str):
        """ Creates a container manager for the given container id

        Arguments:
            docker_client {DockerClient} -- A docker client
            container_id {str} -- the container ID

        Returns:
            ContainerManager -- a container manager for the container
        """
        self.docker_client = docker_client

        self.container_id = container_id

    def __find(self) -> Container:
        for container in self.docker_client.containers.list(all=True):
            if container.id == self.container_id:
                return container
        return None

    def is_running(self) -> bool:
        """ Determines if the container is running

        Raises:
            ContainerNotFound: The container was not found

        Returns:
            bool -- Result
        """
        container = self.__find()

        if not container:
            raise ContainerNotFound

        return bool("running" in container.status)

    def exec(self, command: str, as_user: bool = False, relpath: str = None):
        """ Executes the command in the container

        Arguments:
            command {str} -- The command to run. Usually /bin/bash <>
            relpath {str} -- Relative path to project root to enter before executing. Optional, defaults to none.
        Raises:
            ContainerNotFound: The container was not found
            ContainerNotRunning: The container was not running
        """
        if not self.is_running():
            raise ContainerNotRunning()

        cdto = ENVY_CONFIG.get_project_mount_path()
        if relpath is not None:
            cdto = Path(ENVY_CONFIG.get_project_mount_path(), relpath)

        command_inside_project = "/bin/bash -c 'cd {}; {}'".format(
            cdto, command.replace("'", "'\\''")
        )

        if as_user:
            groups = ",".join(str(x) for x in os.getgroups())
            userspec = str(os.getuid()) + ":" + str(os.getgid())
            command_inside_project = "/usr/sbin/chroot --groups={} --userspec={} / /bin/bash --noprofile -c 'cd {}; {}'".format(
                groups,
                userspec,
                ENVY_CONFIG.get_project_mount_path(),
                command.replace("'", "'\\''"),
            )

        exit_code = dockerpty.exec_command(
            self.docker_client, self.container_id, command_inside_project
        )

        if exit_code != 0:
            raise ContainerError(exit_code)

    def ensure_running(self):
        """ Ensures that the container is running

        Raises:
            ContainerNotFound: The container was not found
        """
        container = self.__find()

        if not container:
            raise ContainerNotFound()

        if "running" not in container.status:
            container.start()

    def ensure_stopped(self):
        """ Ensures that the container is not running

        Raises:
            ContainerNotFound: The container was not found
        """
        container = self.__find()

        if not container:
            raise ContainerNotFound()

        if "running" in container.status:
            container.kill()

    def destroy(self):
        """ Destroys the container
        """
        container = self.__find()

        if container is not None:
            container.remove()
