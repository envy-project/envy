import docker
from lib.docker_helpers.container_finder import ContainerFinder
CLIENT = docker.from_env()
T = ContainerFinder(CLIENT)
