from envy.lib.docker_manager import ContainerManager

from .build_module import BuildModule


class ScriptBuildModule(BuildModule):
    def __init__(self, name: str, container: ContainerManager, steps: [str]):
        super().__init__(name, container)
        self.steps = steps

    def run(self):
        super().run()

        for step in self.steps:
            self.container.exec(step)
