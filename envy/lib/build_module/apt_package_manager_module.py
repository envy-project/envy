from .package_manager_module import PackageManagerModule


class AptPackageManagerModule(PackageManagerModule):
    """ An apt implementation for a Package Manager Module
    """

    def updated_packages(self) -> [str]:
        # TODO: consider changing the implementation to be aware of partial updates
        if self.has_built():
            return self._packages
        return []

    def should_trigger(self) -> bool:
        # TODO: this needs to be implemented before this class is used
        raise NotImplementedError

    def persist_trigger(self):
        # TODO: this needs to be implemented before this class is used
        raise NotImplementedError

    def run(self):
        super().run()
        versioned_packages = [
            "{}={}".format(package["recipe"], package["version"])
            if package["version"]
            else package["recipe"]
            for package in self._packages
        ]

        apt_string = " ".join(
            [versioned_package["recipe"] for versioned_package in versioned_packages]
        )
        self._container.exec(
            "apt-get update && apt-get install -y {} && rm -rf /var/lib/apt/lists/*".format(
                apt_string
            )
        )
