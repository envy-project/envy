from envy.lib.docker_manager import ContainerManager

from .assignable_trigger_step import AssignableTriggerStep


class ScriptSetupStep(AssignableTriggerStep):
    def __init__(self, name: str, container: ContainerManager, scripts: [str]):
        super().__init__(name, container)
        self._scripts = scripts

    def run(self):
        super().run()

        for step in self._scripts:
            self._container.exec(step)
