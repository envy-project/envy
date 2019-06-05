import logging
import tarfile
import io
import os.path
from abc import ABC, abstractmethod
from lib.config.placeholder import getConfigFileHash

class ImageCreator(ABC):
	"""Creates a Docker image, given a set of packages and native executables to run."""

	docker = None
	def __init__(self, docker):
		self.docker = docker

	def createImage(self, packages, nativeExecutables=None):
		#TODO: validate existance of nativeExecutables
		dockerfile = self.buildDockerfile(packages, nativeExecutables)
		tarBytes = self.buildTarballBytes(dockerfile, nativeExecutables)
		image, logs = self.docker.images.build(custom_context=True, tag='envy-' + getConfigFileHash(), rm=True, fileobj=tarBytes)
		logging.info(logs)
		return image.id

	def buildTarballBytes(self, dockerfile, executables=None):
		tarBytes = io.BytesIO()
		tarArchive = tarfile.open(fileobj=tarBytes, mode='x')

		# Write the Dockerfile
		dockerData = dockerfile.encode('utf8')
		info = tarfile.TarInfo(name='Dockerfile')
		info.size = len(dockerData)
		tarArchive.addfile(tarinfo=info, fileobj=io.BytesIO(dockerData))

		#If they exist, add our executables
		if executables is not None:
			def resetName(tarInfo):
				tarInfo.name = os.path.basename(tarInfo.name)
				return tarInfo

			for execute in executables:
				tarArchive.add(execute, filter=resetName)
		# Finish the tar archive
		tarArchive.close()
		#Restore the byte buffer
		tarBytes.seek(0)
		return tarBytes

	def buildDockerfile(self, packages, nativeExecutables=None):
		dFile = 'FROM ' + self.baseImage() + '\n'
		dFile += 'RUN ' + self.getPackageString(packages) + '\n'
		if nativeExecutables is not None:
			for execute in nativeExecutables:
				execute = os.path.basename(execute)
				dFile += 'COPY ' + execute + ' /install/' + execute + '\n'
				dFile += 'RUN chmod a+x /install/' + execute + ' && /install/' + execute + ' && rm /install/' + execute + '\n'
		return dFile

	@abstractmethod
	def baseImage(self):
		pass

	@abstractmethod
	def getPackageString(self, packages):
		pass
