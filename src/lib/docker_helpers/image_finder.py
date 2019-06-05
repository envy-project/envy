import lib.config.placeholder as appConfig
from lib.docker_helpers.apt_image_creator import AptImageCreator

class ImageFinder:
	"""Gets you an image ID for this project - either created fresh or provided by the hash"""
	docker = None
	def __init__(self, docker):
		self.docker = docker

	def findImage(self):
		expectedTag = 'envy-" + appConfig.getConfigFileHash()
		images = self.docker.images.list()
		for image in images:
			if expectedTag in image.tags:
				return image.id
		# TODO: Use the correct image creator based on the config file!
		aic = AptImageCreator(self.docker)

		#TODO: packages need to be made more portable
		return aic.createImage(appConfig.getNeededPackages(), appConfig.getExtraExecutables())
