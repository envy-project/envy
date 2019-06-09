import docker
import dockerpty

from envy.lib.docker_helpers.container_finder import ContainerFinder

CLIENT = docker.from_env()
T = ContainerFinder(CLIENT)
CONTAINER = T.findAndEnsureRunning()

dockerpty.exec_command(CLIENT, CONTAINER.id, "/bin/bash")
