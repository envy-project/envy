from lib.docker_helpers.image_finder import ImageFinder
import docker
client = docker.from_env()
t = ImageFinder(client)
print(t.findImage())

