from lib.docker_helpers.container_finder import ContainerFinder
import docker
client = docker.from_env()
t = ContainerFinder(client)
t.destroyContainer()
t.findAndEnsureRunning()

