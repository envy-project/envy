import docker
import dockerpty

from envy.lib.docker_helpers.container_finder import ContainerFinder

CLIENT = docker.from_env()
T = ContainerFinder(CLIENT)
CONTAINER = T.find_and_ensure_running()

dockerpty.exec_command(CLIENT, CONTAINER.id, "/bin/bash")
