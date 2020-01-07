from envy.lib.docker_manager import ContainerManager

from .assignable_trigger_step import AssignableTriggerStep


class ScriptSetupStep(AssignableTriggerStep):
    def __init__(
        self,
        name: str,
        container: ContainerManager,
        scripts: [str],
        as_user: bool = True,
    ):
        super().__init__(name, container)
        self._scripts = scripts
        self._as_user = as_user

    def run(self):
        super().run()

        if isinstance(self._scripts, str):
            self._container.exec(self._scripts, self._as_user)
        else:
            for step in self._scripts:
                self._container.exec(step, self._as_user)
