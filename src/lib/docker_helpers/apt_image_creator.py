from lib.docker_helpers.image_creator import ImageCreator

class AptImageCreator(ImageCreator):
	def baseImage(self):
		return 'ubuntu:19.04'

	def getPackageString(self, packages):
		# TODO: validation here to ensure shell safety
		aptString = " ".join(packages)
		return 'apt-get update && apt-get install -y ' + aptString + ' && rm -rf /var/lib/apt/lists/*'
