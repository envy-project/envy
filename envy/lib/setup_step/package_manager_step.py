from abc import abstractmethod

from envy.lib.docker_manager import ContainerManager

from .setup_step import SetupStep


class PackageManagerStep(SetupStep):
    """ A Package Manager Step is a Build Step that repesents a step that handles
    system package dependencies for an ENVy environment image.
    """

    def __init__(self, container: ContainerManager, packages: [{}]):
        super(PackageManagerStep, self).__init__(
            "System Packages", "Installing System Packages", container
        )
        self._packages = packages

    @abstractmethod
    def updated_packages(self) -> [str]:
        """ Return a list of packages that were changed or freshly installed
        If called before the step is run, will return an empty list
        """
        if self.has_built():
            return self._packages
        return []
