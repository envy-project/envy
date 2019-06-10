import docker

from envy.lib.state import ENVY_STATE

from .connection_tester import ConnectionTester
from .container_manager import ContainerManager
from .image_manager import ImageManager


class ContainerExists(Exception):
    pass


class ImageExists(Exception):
    pass


class ImageNotFound(Exception):
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

        self.ensure_image()

        return self.create_container()

    def ensure_image(self) -> ImageManager:
        """ Ensures that an ENVy image exists.
            If no valid image is found, creates a new image and writes it to the state.

        Returns:
            ImageManager -- An image manager for the ensured image
        """
        image = self.get_image()

        if image:
            return image

        return self.create_image()

    ### CREATE ###
    def create_container(self) -> ContainerManager:
        """ Creates an ENVy container. Requires that the container does not already exist, and that the image already exists.

        Raises:
            ContainerExists: The container ID specified in ENVY_STATE already exists.
            ImageNotFound: The image ID specified in ENVY_STATE was not found.

        Returns:
            ContainerManager -- A container manager for the newly created container
        """
        if self.get_container():
            raise ContainerExists()

        if not self.get_image():
            raise ImageNotFound()

        container_manager = ContainerManager.create(
            self.docker_client, ENVY_STATE.get_image_id()
        )

        ENVY_STATE.set_container_id(container_manager.container_id)

        return container_manager

    def create_image(self) -> ImageManager:
        """ Creates an ENVy image. Requires that the image does not already exist.

        Raises:
            ImageExists: The image ID specified in ENVY_STATE already exists.

        Returns:
            ImageManager -- An image manager for the newly created image
        """
        if self.get_image():
            raise ImageExists()

        image_manager = ImageManager.create(self.docker_client)

        ENVY_STATE.set_image_id(image_manager.image_id)

        return image_manager

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

    def get_image(self) -> ImageManager:
        """ Returns an image manager for the image specified in ENVY_STATE

        Returns:
            ImageManager -- The image manager
        """
        image_id = ENVY_STATE.get_image_id()

        if image_id:
            return ImageManager(self.docker_client, ENVY_STATE.get_image_id())
        return None

    ### NUKE ###
    def nuke(self):
        """ Stops and deletes the container and image found in ENVY_STATE
        """
        container = self.get_container()
        image = self.get_image()

        if container:
            container.ensure_stopped()
            container.destroy()
        if image:
            image.destroy()

        ENVY_STATE.set_container_id("")
        ENVY_STATE.set_image_id("")
