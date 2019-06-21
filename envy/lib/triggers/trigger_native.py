from envy.lib.build_module.package_manager_module import PackageManagerModule

from .trigger import Trigger


class TriggerNative(Trigger):
    """ Triggers whenever the given native dependency is reinstalled.
        NOTE: Currently we don't reinstall native dependencies piecemeal, so this triggers whenever the image is rebuilt.
    """

    def __init__(self, recipe: str, package_manager_module: PackageManagerModule):
        self.recipe = recipe
        self.package_manager_module = package_manager_module

    def should_trigger(self) -> bool:
        if self.recipe in [
            package["recipe"]
            for package in self.package_manager_module.updated_packages()
        ]:
            return True
        return False

    def persist_trigger(self):
        pass
