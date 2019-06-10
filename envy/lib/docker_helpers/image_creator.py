import logging
import tarfile
import io
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

    def build_image_tag(self):
        return "envy-{}".format(ENVY_CONFIG.get_environment_hash())

    def create_image(self, packages, native_executables=None):
        """ Create a docker image from a set of packages and executables.
            NOTE: currently not validating either packages or executables
            Args:
                packages (list<string>): A list of packages to install
                native_executables(list<ConfigExecFile>): A list of ConfigExecFiles to install into the image.
            Returns:
                string: the Docker image ID
        """
        # TODO: validate existance of native_executables
        dockerfile = self.build_dockerfile(packages, native_executables)
        tar_bytes = self.build_tarball_bytes(dockerfile, native_executables)
        image, logs = self.docker.images.build(
            custom_context=True, tag=self.build_image_tag(), rm=True, fileobj=tar_bytes
        )
        logging.info(logs)
        return image.id

    def build_tarball_bytes(self, dockerfile, executables=None):
        """ Build a tarball BytesIO with the Dockerfile, and include all passed-in executables
            NOTE: no validation is performed for malicious content!
            Args:
                dockerfile (string): the Dockerfile you want to include
                executables (list<string>): Absolute paths to the executables you want. They will be included in the root of the tar archive as their basename.
            Returns:
                BytesIO: A bytes IO object that represents an uncompressed tarball, ready to be passed to Docker.
        """
        tar_bytes = io.BytesIO()
        tar_archive = tarfile.open(fileobj=tar_bytes, mode="x")

        # Write the Dockerfile
        docker_data = dockerfile.encode("utf8")
        info = tarfile.TarInfo(name="Dockerfile")
        info.size = len(docker_data)
        tar_archive.addfile(tarinfo=info, fileobj=io.BytesIO(docker_data))

        # If they exist, add our executables
        if executables:
            for execute in executables:
                info = tarfile.TarInfo(name=execute.filename)
                info.size = len(execute.bytes)
                tar_archive.addfile(tarinfo=info, fileobj=io.BytesIO(execute.bytes))
        # Finish the tar archive
        tar_archive.close()
        # Restore the byte buffer
        tar_bytes.seek(0)
        return tar_bytes

    def build_dockerfile(self, packages, native_executables=None):
        """ Create a Dockerfile that will result in a reasonable number of layers.
            NOTE: no validation performed on package names or native executables
            Args:
                packages (list<string>): The packages you want to install
                native_executables (list<string>): The native executables you want to run to provision the image
            Returns:
                string: the string representation of the Dockerfile
        """
        d_file = "FROM " + self.base_image() + "\n"
        d_file += "RUN " + self.get_package_string(packages) + "\n"
        if native_executables:
            for execute in native_executables:
                execute = execute.filename
                d_file += "COPY " + execute + " /install/" + execute + "\n"
                d_file += (
                    "RUN chmod a+x /install/"
                    + execute
                    + " && /install/"
                    + execute
                    + " && rm /install/"
                    + execute
                    + "\n"
                )
        return d_file

    @abstractmethod
    def base_image(self):
        pass

    @abstractmethod
    def get_package_string(self, packages):
        pass
