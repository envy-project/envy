import logging
import tarfile
import io
from abc import ABC, abstractmethod

from envy.lib.config import ENVY_CONFIG


class ImageCreator(ABC):
    """ Creates a Docker image, given a set of packages.
        This is an abstract class - you may want an AptImageCreator for now.
        See also: ImageFinder
        Args:
            docker (Client): A Docker client
    """

    docker = None

    def __init__(self, docker):
        self.docker = docker

    def build_image_tag(self):
        return "envy-{}".format(ENVY_CONFIG.get_image_hash())

    def create_image(self, packages: [str]):
        """ Create a docker image from a set of packages.
            NOTE: currently not validating packages, or respecting versions

        Argsuments:
            packages (list<string>): A list of packages to install

        Returns:
            string: the Docker image ID
        """
        dockerfile = self.build_dockerfile(packages)
        tar_bytes = self.build_tarball_bytes(dockerfile)
        image, logs = self.docker.images.build(
            custom_context=True, tag=self.build_image_tag(), rm=True, fileobj=tar_bytes
        )
        logging.info(logs)
        return image.id

    def build_tarball_bytes(self, dockerfile):
        """ Build a tarball BytesIO with the Dockerfile
            NOTE: no validation is performed for malicious content!
            Args:
                dockerfile (string): the Dockerfile you want to include
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

        # Finish the tar archive
        tar_archive.close()
        # Restore the byte buffer
        tar_bytes.seek(0)
        return tar_bytes

    def build_dockerfile(self, packages):
        """ Create a Dockerfile that will result in a reasonable number of layers.
            NOTE: no validation performed on package names
            Args:
                packages (list<string>): The packages you want to install
            Returns:
                string: the string representation of the Dockerfile
        """
        d_file = f"FROM {ENVY_CONFIG.get_base_image()}\n"
        d_file += f"RUN {self.get_package_string(packages)}\n"
        return d_file

    @abstractmethod
    def get_package_string(self, packages):
        pass
