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
        self.image_finder = ImageFinder(docker)

    def generate_container_name(self):
        return "envy-" + ENVY_CONFIG.get_environment_hash() + "-container"

    def find_and_ensure_running(self):
        """ Find a container and ensure that the container is running
            Returns:
                The docker container object, in a running state
        """
        container = self.find_container()
        if container is not None and "running" not in container.status:
            container.start()
        return container

    def find_and_ensure_stopped(self):
        """ Find a container and ensure that the container is stopped
            Returns:
                The docker container object, in a stopped state
        """
        container = self.find_container()
        if container is not None and "running" in container.status:
            container.kill()
        return container

    def destroy_container(self):
        """ Find the container for this project and destroy it
        """
        container = self.find_and_ensure_stopped()
        if container is None:
            return

        container.remove()
        ENVY_STATE.set_container_id("")

    def find_container(self):
        """ Find the container to use for this project. You probably want the findAndEnsure* methods instead.
            Returns:
                Docker container object in an undefined state
        """
        expected_container_id = ENVY_STATE.get_container_id()

        if expected_container_id:
            containers = self.docker.containers.list(all=True)
            for container in containers:
                if container.id == expected_container_id:
                    return container
        return None

    def find_or_create_container(self):
        existing_container = self.find_container()
        if existing_container is not None:
            return existing_container

        image_id = self.image_finder.find_or_create_image()

        logging.info("Creating new container for: %s", image_id)
        print("Creating ENVy container")

        project_mount = Mount(
            "/project", str(ENVY_CONFIG_FILE_PATH.parent), type="bind"
        )
        docker_socket_mount = Mount(
            "/var/run/docker.sock", "/var/run/docker.sock", type="bind"
        )
        container = self.docker.containers.create(
            image_id,
            "tail -f /dev/null",
            name=self.generate_container_name(),
            mounts=[project_mount, docker_socket_mount],
        )

        ENVY_STATE.set_container_id(container.id)
        return container
