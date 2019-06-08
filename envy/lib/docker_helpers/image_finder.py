import envy.lib.config.placeholder as appConfig
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
        self.docker.images.remove(image=imgId)

    def findImage(self):
        """ Create a docker image
            Returns:
                string: The Docker image ID
        """
        expectedTag = "envy-" + appConfig.getConfigFileHash()
        images = self.docker.images.list()
        for image in images:
            if expectedTag in image.tags:
                return image.id
        # TODO: Use the correct image creator based on the config file!
        aic = AptImageCreator(self.docker)

        # TODO: packages need to be made more portable
        return aic.createImage(
            appConfig.getNeededPackages(), appConfig.getExtraExecutables()
        )
