import docker
from lib.docker_helpers.container_finder import ContainerFinder
import dockerpty

CLIENT = docker.from_env()
T = ContainerFinder(CLIENT)
CONTAINER = T.findAndEnsureRunning()

dockerpty.exec_command(CLIENT, CONTAINER.id, "/bin/bash")
