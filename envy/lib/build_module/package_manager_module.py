from abc import abstractmethod

from envy.lib.docker_manager import ContainerManager

from .build_module import BuildModule


class PackageManagerModule(BuildModule):
    """ A Package Manager Module is a Build Module that repesents a step that handles
    packaged, native dependencies for an ENVy environment image.
    """

    def __init__(self, name: str, container: ContainerManager, packages: [{}]):
        super(PackageManagerModule, self).__init__(name, container)
        self._packages = packages

    @abstractmethod
    def updated_packages(self) -> [str]:
        """ Return a list of packages that were changed or freshly installed
        If called before the module is run, will return an empty list
        """
        if self.has_built():
            return self._packages
        return []
