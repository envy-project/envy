import logging
import tarfile
import io
import os.path
from abc import ABC, abstractmethod

from envy.lib.config import ENVY_CONFIG


class ImageCreator(ABC):
    """ Creates a Docker image, given a set of packages and native executables to run.
        This is an abstract class - you may want an AptImageCreator for now.
        See also: ImageFinder
        Args:
            docker (Client): A Docker client
    """

    docker = None

    def __init__(self, docker):
        self.docker = docker

    def buildImageTag(self):
        return "envy-{}".format(ENVY_CONFIG.getEnvironmentHash())

    def createImage(self, packages, nativeExecutables=None):
        """ Create a docker image from a set of packages and executables.
            NOTE: currently not validating either packages or executables
            Args:
                packages (list<string>): A list of packages to install
                nativeExecutables(list<ConfigExecFile>): A list of ConfigExecFiles to install into the image.
            Returns:
                string: the Docker image ID
        """
        # TODO: validate existance of nativeExecutables
        dockerfile = self.buildDockerfile(packages, nativeExecutables)
        tarBytes = self.buildTarballBytes(dockerfile, nativeExecutables)
        image, logs = self.docker.images.build(
            custom_context=True, tag=self.buildImageTag(), rm=True, fileobj=tarBytes
        )
        logging.info(logs)
        return image.id

    def buildTarballBytes(self, dockerfile, executables=None):
        """ Build a tarball BytesIO with the Dockerfile, and include all passed-in executables
            NOTE: no validation is performed for malicious content!
            Args:
                dockerfile (string): the Dockerfile you want to include
                executables (list<string>): Absolute paths to the executables you want. They will be included in the root of the tar archive as their basename.
            Returns:
                BytesIO: A bytes IO object that represents an uncompressed tarball, ready to be passed to Docker.
        """
        tarBytes = io.BytesIO()
        tarArchive = tarfile.open(fileobj=tarBytes, mode="x")

        # Write the Dockerfile
        dockerData = dockerfile.encode("utf8")
        info = tarfile.TarInfo(name="Dockerfile")
        info.size = len(dockerData)
        tarArchive.addfile(tarinfo=info, fileobj=io.BytesIO(dockerData))

        # If they exist, add our executables
        if executables:
            for execute in executables:
                info = tarfile.TarInfo(name=execute.filename)
                info.size = len(execute.bytes)
                tarArchive.addfile(tarinfo=info, fileobj=io.BytesIO(execute.bytes))
        # Finish the tar archive
        tarArchive.close()
        # Restore the byte buffer
        tarBytes.seek(0)
        return tarBytes

    def buildDockerfile(self, packages, nativeExecutables=None):
        """ Create a Dockerfile that will result in a reasonable number of layers.
            NOTE: no validation performed on package names or native executables
            Args:
                packages (list<string>): The packages you want to install
                nativeExecutables (list<string>): The native executables you want to run to provision the image
            Returns:
                string: the string representation of the Dockerfile
        """
        dFile = "FROM " + self.baseImage() + "\n"
        dFile += "RUN " + self.getPackageString(packages) + "\n"
        if nativeExecutables:
            for execute in nativeExecutables:
                execute = execute.filename
                dFile += "COPY " + execute + " /install/" + execute + "\n"
                dFile += (
                    "RUN chmod a+x /install/"
                    + execute
                    + " && /install/"
                    + execute
                    + " && rm /install/"
                    + execute
                    + "\n"
                )
        return dFile

    @abstractmethod
    def baseImage(self):
        pass

    @abstractmethod
    def getPackageString(self, packages):
        pass
