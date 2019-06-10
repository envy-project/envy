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
    def __init__(self):
        self.docker_client = docker.from_env()

        self.tester = ConnectionTester(self.docker_client)

    ### DOCKER CONNECTION ###
    def connection_ok(self):
        return self.tester.ok()

    def print_connection_err(self):
        self.tester.print_err()

    ### ENSURE ###
    def ensure_container(self):
        container = self.get_container()

        if container:
            return container

        self.ensure_image()

        return self.create_container()

    def ensure_image(self):
        image = self.get_image()

        if image:
            return image

        return self.create_image()

    ### CREATE ###
    def create_container(self):
        if self.get_container():
            raise ContainerExists()

        if not self.get_image():
            raise ImageNotFound()

        container_manager = ContainerManager.create(
            self.docker_client, ENVY_STATE.get_image_id()
        )

        ENVY_STATE.set_container_id(container_manager.container_id)

        return container_manager

    def create_image(self):
        if self.get_image():
            raise ImageExists()

        image_manager = ImageManager.create(self.docker_client)

        ENVY_STATE.set_image_id(image_manager.image_id)

        return image_manager

    ### GET ###
    def get_container(self):
        container_id = ENVY_STATE.get_container_id()

        if container_id:
            return ContainerManager(self.docker_client, ENVY_STATE.get_container_id())
        return None

    def get_image(self):
        image_id = ENVY_STATE.get_image_id()

        if image_id:
            return ImageManager(self.docker_client, ENVY_STATE.get_image_id())
        return None

    ### NUKE ###
    def nuke(self):
        container = self.get_container()
        image = self.get_image()

        if container:
            container.ensure_stopped()
            container.destroy()
        if image:
            image.destroy()

        ENVY_STATE.set_container_id("")
        ENVY_STATE.set_image_id("")
