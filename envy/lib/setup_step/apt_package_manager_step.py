from envy.lib.state import ENVY_STATE

from .package_manager_step import PackageManagerStep


class AptPackageManagerStep(PackageManagerStep):
    """ An apt implementation for a Package Manager Step
    """

    def updated_packages(self) -> [str]:
        # TODO: consider changing the implementation to be aware of partial updates
        if self.has_built():
            return self._packages
        return []

    def should_trigger(self) -> bool:
        return ENVY_STATE.get_installed_packages() != self._packages

    def persist_trigger(self):
        ENVY_STATE.set_installed_packages(self._packages)

    def run(self):
        super().run()
        versioned_packages = [
            "{}={}".format(package["recipe"], package["version"])
            if "version" in package
            else package["recipe"]
            for package in self._packages
        ]

        apt_string = " ".join(
            [versioned_package for versioned_package in versioned_packages]
        )
        self._container.exec(
            "apt-get update && apt-get install -y {} && rm -rf /var/lib/apt/lists/*".format(
                apt_string
            )
        )
