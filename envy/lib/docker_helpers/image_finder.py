from envy.lib.config import ENVY_CONFIG
from envy.lib.state import ENVY_STATE
from envy.lib.docker_helpers.apt_image_creator import AptImageCreator


class ImageFinder:
    """ Gets you an image ID for this project - either created fresh or already created and identified by the hash.
        See also: ContainerFinder
        Args:
            docker (Client): A Docker client

    """

    docker = None

    def __init__(self, docker):
        self.docker = docker

    def destroyImage(self):
        """ Destroy the image, if it existed """
        imgId = self.findImage()
        if imgId is None:
            return

        self.docker.images.remove(image=imgId)

    def findImage(self):
        """ Create a docker image
            Returns:
                string: The Docker image ID
        """
        expectedID = ENVY_STATE.getImageID()
        images = self.docker.images.list()
        for image in images:
            if image.id == expectedID:
                return image.id
        return None

    def findOrCreateImage(self):
        existingImage = self.findImage()
        if existingImage is not None:
            return existingImage

        print("Building ENVy environment image")

        # TODO: Use the correct image creator based on the config file!
        aic = AptImageCreator(self.docker)

        # TODO: packages need to be made more portable
        image_id = aic.createImage(
            ENVY_CONFIG.getNativeDependencies(), ENVY_CONFIG.getExtraExecutables()
        )

        ENVY_STATE.setImageID(image_id)

        return image_id
