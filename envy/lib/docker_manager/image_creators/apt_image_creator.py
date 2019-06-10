from .image_creator import ImageCreator


class AptImageCreator(ImageCreator):
    def base_image(self):
        return "ubuntu:18.04"

    def get_package_string(self, packages):
        # TODO: validation here to ensure shell safety
        apt_string = " ".join([package["recipe"] for package in packages])
        return "apt-get update && apt-get install -y {} && rm -rf /var/lib/apt/lists/*".format(
            apt_string
        )
