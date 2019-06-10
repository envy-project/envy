from envy.lib.config import ENVY_CONFIG
from envy.lib.file_downloader import resolve_files

from .image_creators import AptImageCreator


class ImageManager:
    ### Static Image Creation ###
    @staticmethod
    def create(docker_client):
        print("Creating ENVy environment image.")

        # TODO: Use the correct image creator based on the config file!
        image_id = AptImageCreator(docker_client).create_image(
            ENVY_CONFIG.get_native_dependencies(),
            resolve_files(ENVY_CONFIG.get_extra_executables()),
        )

        return ImageManager(docker_client, image_id)

    ### Image Management ###
    def __init__(self, docker_client, image_id):
        self.docker_client = docker_client

        self.image_id = image_id

    def __find(self):
        for image in self.docker_client.images.list():
            if image.id == self.image_id:
                return image
        return None

    def destroy(self):
        if self.image_id and self.__find():
            self.docker_client.images.remove(self.image_id)
