from docker import DockerClient
from docker.models.images import Image

from envy.lib.config import ENVY_CONFIG

from .image_creators import AptImageCreator


class ImageManager:
    ### Static Image Creation ###
    @staticmethod
    def create(docker_client: DockerClient) -> "ImageManager":
        """ Creates an image from the ENVY_CONFIG environment

        Arguments:
            docker_client {DockerClient} -- A docker client

        Returns:
            [ImageManager] -- an image manager for the created image
        """
        print("Creating ENVy environment image.")

        # TODO: Use the correct image creator based on the config file's base image
        image_id = AptImageCreator(docker_client).create_image(
            ENVY_CONFIG.get_native_dependencies()
        )

        return ImageManager(docker_client, image_id)

    ### Image Management ###
    def __init__(self, docker_client: DockerClient, image_id: str):
        """ Creates an image manager for the given image id

        Arguments:
            docker_client {DockerClient} -- A docker client
            image_id {str} -- the image ID

        Returns:
            ImageManager -- an image manager for the created image
        """
        self.docker_client = docker_client

        self.image_id = image_id

    def __find(self) -> Image:
        for image in self.docker_client.images.list():
            if image.id == self.image_id:
                return image
        return None

    def destroy(self):
        """ Destroys the image
        """
        if self.image_id and self.__find():
            self.docker_client.images.remove(self.image_id)
