import logging
from docker.types import Mount

import lib.config.placeholder as appConfig
from lib.docker_helpers.image_finder import ImageFinder

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

	def expectedLabel(self):
		return 'envy-' + appConfig.getConfigFileHash() + '-container'

	def findAndEnsureRunning(self):
		""" Find a container and ensure that the container is running
			Returns:
				The docker container object, in a running state
		"""
		container = self.findContainer()
		if 'running' not in container.status:
			container.start()
		return container

	def findAndEnsureStopped(self):
		""" Find a container and ensure that the container is stopped
			Returns:
				The docker container object, in a stopped state
		"""
		container = self.findContainer()
		if 'running' in container.status:
			container.kill()
		return container

	def destroyContainer(self):
		""" Find the container for this project and destroy it
		"""
		container = self.findAndEnsureStopped()
		container.remove()

	def findContainer(self):
		""" Find the container to use for this project. You probably want the findAndEnsure* methods instead.
			Returns:
				Docker container object in an undefined state
		"""
		expectedLabel = self.expectedLabel()
		containers = self.docker.containers.list(all=True)
		for container in containers:
			if container.name == expectedLabel:
				return container
		imageId = self.imageFinder.findImage()
		logging.info('Creating new container for: %s', imageId)
		projectMount = Mount('/project', appConfig.getProjectBasePath(), type='bind')
		container = self.docker.containers.create(imageId, 'tail -f /dev/null', name=expectedLabel, mounts=[projectMount])
		return container
