from envy.lib.setup_step.package_manager_step import PackageManagerStep

from .trigger import Trigger


class TriggerSystemPackage(Trigger):
    """ Triggers whenever the given system package is reinstalled.
        NOTE: Currently we don't reinstall system packages piecemeal, so this triggers whenever any package changes
    """

    def __init__(self, recipe: str, package_manager_step: PackageManagerStep):
        self.recipe = recipe
        self.package_manager_step = package_manager_step

    def should_trigger(self) -> bool:
        if self.recipe in [
            package["recipe"]
            for package in self.package_manager_step.updated_packages()
        ]:
            return True
        return False

    def persist_trigger(self):
        pass
