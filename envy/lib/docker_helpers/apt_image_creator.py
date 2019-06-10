from envy.lib.docker_helpers.image_creator import ImageCreator


class AptImageCreator(ImageCreator):
    def baseImage(self):
        return "ubuntu:18.04"

    def getPackageString(self, packages):
        # TODO: validation here to ensure shell safety
        aptString = " ".join([package["recipe"] for package in packages])
        return "apt-get update && apt-get install -y {} && rm -rf /var/lib/apt/lists/*".format(
            aptString
        )
