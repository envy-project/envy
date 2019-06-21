from envy.lib.docker_manager import ContainerManager

from .build_module import BuildModule


class RemoteBuildModule(BuildModule):
    def __init__(self, name: str, container: ContainerManager, url: str):
        super().__init__(name, container)
        self.url = url

    def run(self):
        super().run()

        print("WARNING: Remote Build Modules not implemented!")  # TODO
