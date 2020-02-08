import docker

from envy.lib.config import ENVY_CONFIG
from envy.lib.state import ENVY_STATE

from .connection_tester import ConnectionTester
from .container_manager import ContainerManager


class ContainerExists(Exception):
    pass


class DockerManager:
    """ Manages the docker connection, and handles creation and acquisition of containers and images.
        Gets the docker client from env (docker.from_env()) automatically when created.
        You probably want to run connection_ok() to verify that docker is available, since we're not throwing in the constructor.
    """

    def __init__(self):
        self.docker_client = docker.from_env()

        self.tester = ConnectionTester(self.docker_client)

    ### DOCKER CONNECTION ###
    def connection_ok(self) -> bool:
        """ Returns the result of the docker connection test
        Returns:
            bool -- The result of the connection test
        """
        return self.tester.ok()

    def print_connection_err(self):
        """ Prints an error message for a failed docker connection.
        """
        self.tester.print_err()

    ### ENSURE ###
    def ensure_container(self) -> ContainerManager:
        """ Ensures that an ENVy container exists.
            If no valid container is found, creates a new container and writes it to the state.
            This ensures that a valid image exists as well.

        Returns:
            ContainerManager -- A container manager for the ensured container
        """
        container = self.get_container()

        if container:
            return container

        return self.create_container()

    ### CREATE ###
    def create_container(self) -> ContainerManager:
        """ Creates an ENVy container. Requires that the container does not already exist, and that the image already exists.

        Raises:
            ContainerExists: The container ID specified in ENVY_STATE already exists.

        Returns:
            ContainerManager -- A container manager for the newly created container
        """
        if self.get_container():
            raise ContainerExists()

        image = ENVY_CONFIG.get_base_image()
        if ":" not in image:
            image += ":latest"

        try:
            self.docker_client.images.get(image)
        except docker.errors.ImageNotFound:
            print("Pulling base image, this may take a while...")

        self.docker_client.images.pull(image)

        container_manager = ContainerManager.create(self.docker_client, image)

        ENVY_STATE.set_container_id(container_manager.container_id)

        return container_manager

    ### GET ###
    def get_container(self) -> ContainerManager:
        """ Returns a container manager for the container specified in ENVY_STATE

        Returns:
            ContainerManager -- The container manager
        """
        container_id = ENVY_STATE.get_container_id()

        if container_id:
            return ContainerManager(self.docker_client, ENVY_STATE.get_container_id())
        return None

    ### NUKE ###
    def nuke(self):
        """ Stops and deletes the container found in ENVY_STATE
        """
        container = self.get_container()

        if container:
            container.ensure_stopped()
            container.destroy()

        ENVY_STATE.set_container_id("")
