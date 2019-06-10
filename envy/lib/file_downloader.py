import requests


class ConfigExecFile:
    def __init__(self, filename, byt):
        self.filename = filename
        self.bytes = byt


class FileDownloadError(Exception):
    def __init__(self, requests_error):
        super(FileDownloadError, self).__init__()
        self.requests_error = requests_error


def resolve_files(file_objects):
    """ Turn file objects from the config into "real" objects with Byte strings. Currently only supports URL format
        Args:
            file_objects (list<dict>): file_objects from the config
        Returns:
            list<ConfigExecFile>: List of executable files to run in the image
        Raises:
            FileDownloadError: When a file fails to download for some reason. Contains the Requests error.
    """
    if not file_objects:
        return None
    returned_list = []
    for obj in file_objects:
        try:
            r = requests.get(obj["url"])
            returned_list.append(ConfigExecFile(obj["filename"], r.content))
        except requests.exceptions.RequestException as e:
            raise FileDownloadError(e)
    return returned_list
