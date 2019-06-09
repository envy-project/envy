import logging
from docker.types import Mount

from envy.lib.config import ENVY_CONFIG_FILE_PATH, ENVY_CONFIG
from envy.lib.state import ENVY_STATE
from envy.lib.docker_helpers.image_finder import ImageFinder


class ContainerFinder:
    """ Class to assist in finding a Docker container.
        Will build image if it has not already been built.
        See also: ImageFinder
        Args:
            docker (Client): A docker client
    """

    docker = None

    def __init__(self, docker):
        self.docker = docker
        self.imageFinder = ImageFinder(docker)

    def generateContainerName(self):
        return "envy-" + ENVY_CONFIG.getEnvironmentHash() + "-container"

    def findAndEnsureRunning(self):
        """ Find a container and ensure that the container is running
            Returns:
                The docker container object, in a running state
        """
        container = self.findContainer()
        if container is not None and "running" not in container.status:
            container.start()
        return container

    def findAndEnsureStopped(self):
        """ Find a container and ensure that the container is stopped
            Returns:
                The docker container object, in a stopped state
        """
        container = self.findContainer()
        if container is not None and "running" in container.status:
            container.kill()
        return container

    def destroyContainer(self):
        """ Find the container for this project and destroy it
        """
        container = self.findAndEnsureStopped()
        if container is None:
            return

        container.remove()
        ENVY_STATE.setContainerID("")

    def findContainer(self):
        """ Find the container to use for this project. You probably want the findAndEnsure* methods instead.
            Returns:
                Docker container object in an undefined state
        """
        expectedContainerID = ENVY_STATE.getContainerID()

        if expectedContainerID:
            containers = self.docker.containers.list(all=True)
            for container in containers:
                if container.id == expectedContainerID:
                    return container
        return None

    def findOrCreateContainer(self):
        existingContainer = self.findContainer()
        if existingContainer is not None:
            return existingContainer

        imageId = self.imageFinder.findOrCreateImage()

        logging.info("Creating new container for: %s", imageId)
        print("Creating ENVy container")

        projectMount = Mount("/project", str(ENVY_CONFIG_FILE_PATH.parent), type="bind")
        dockerSocketMount = Mount(
            "/var/run/docker.sock", "/var/run/docker.sock", type="bind"
        )
        container = self.docker.containers.create(
            imageId,
            "tail -f /dev/null",
            name=self.generateContainerName(),
            mounts=[projectMount, dockerSocketMount],
        )

        ENVY_STATE.setContainerID(container.id)
        return container
