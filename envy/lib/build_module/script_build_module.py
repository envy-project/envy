from envy.lib.docker_manager import ContainerManager

from .assignable_trigger_module import AssignableTriggerModule


class ScriptBuildModule(AssignableTriggerModule):
    def __init__(self, name: str, container: ContainerManager, steps: [str]):
        super().__init__(name, container)
        self._steps = steps

    def run(self):
        super().run()

        for step in self._steps:
            self._container.exec(step)
