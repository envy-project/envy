from docker.types import Mount
import dockerpty

from envy.lib.config import ENVY_CONFIG_FILE_PATH, ENVY_CONFIG


class ContainerNotFound(Exception):
    pass


class ContainerNotRunning(Exception):
    pass


class ContainerManager:
    ### Static Container Creation ###
    @staticmethod
    def __generate_container_name():
        return "envy-" + ENVY_CONFIG.get_environment_hash() + "-container"

    @staticmethod
    def create(docker_client, image_id):
        print("Creating ENVy container")

        container = docker_client.containers.create(
            image_id,
            "tail -f /dev/null",
            name=ContainerManager.__generate_container_name(),
            mounts=[
                Mount("/project", str(ENVY_CONFIG_FILE_PATH.parent), type="bind"),
                Mount("/var/run/docker.sock", "/var/run/docker.sock", type="bind"),
            ],
        )

        return ContainerManager(docker_client, container.id)

    ### Container Management ###
    def __init__(self, docker_client, container_id):
        self.docker_client = docker_client

        self.container_id = container_id

    def __find(self):
        for container in self.docker_client.containers.list(all=True):
            if container.id == self.container_id:
                return container
        return None

    def is_running(self):
        container = self.__find()

        if not container:
            raise ContainerNotFound

        return bool("running" in container.status)

    def exec(self, command):
        if not self.is_running():
            raise ContainerNotRunning()

        dockerpty.exec_command(self.docker_client, self.container_id, command)

    def ensure_running(self):
        container = self.__find()

        if not container:
            raise ContainerNotFound()

        if "running" not in container.status:
            container.start()

    def ensure_stopped(self):
        container = self.__find()

        if not container:
            raise ContainerNotFound()

        if "running" in container.status:
            container.kill()

    def destroy(self):
        container = self.__find()

        if container is not None:
            container.remove()
