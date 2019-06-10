from envy.lib.config import ENVY_CONFIG
from envy.lib.state import ENVY_STATE
from envy.lib.docker_helpers.apt_image_creator import AptImageCreator
from envy.lib.file_downloader import resolve_files


class ImageFinder:
    """ Gets you an image ID for this project - either created fresh or already created and identified by the hash.
        See also: ContainerFinder
        Args:
            docker (Client): A Docker client

    """

    docker = None

    def __init__(self, docker):
        self.docker = docker

    def destroy_image(self):
        """ Destroy the image, if it existed """
        image_id = self.find_image()
        if image_id is None:
            return

        self.docker.images.remove(image=image_id)

    def find_image(self):
        """ Create a docker image
            Returns:
                string: The Docker image ID
        """
        expected_id = ENVY_STATE.get_image_id()
        images = self.docker.images.list()
        for image in images:
            if image.id == expected_id:
                return image.id
        return None

    def find_or_create_image(self):
        existing_image = self.find_image()
        if existing_image is not None:
            return existing_image

        print("Building ENVy environment image")

        # TODO: Use the correct image creator based on the config file!
        aic = AptImageCreator(self.docker)

        # TODO: packages need to be made more portable
        image_id = aic.create_image(
            ENVY_CONFIG.get_native_dependencies(),
            resolve_files(ENVY_CONFIG.get_extra_executables()),
        )

        ENVY_STATE.set_image_id(image_id)

        return image_id
