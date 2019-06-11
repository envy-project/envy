import requests
from envy.lib.config.file import find_project_root


class ConfigExecFile:
    def __init__(self, filename, byt):
        self.filename = filename
        self.bytes = byt


class FileDownloadError(Exception):
    def __init__(self, requests_error):
        super(FileDownloadError, self).__init__()
        self.requests_error = requests_error


def resolve_files(file_objects):
    """ Turn file objects from the config into "real" objects with Byte strings.
        Support URL and path formats
        Args:
            file_objects (list<dict>): fileObjects from the config
        Returns:
            list<ConfigExecFile>: List of executable files to run in the image
        Raises:
            FileDownloadError: When a file fails to download for some reason. Contains the Requests error.
    """
    if not file_objects:
        return None
    project_root = find_project_root()
    returned_list = []
    for obj in file_objects:
        try:
            if "url" in obj:
                r = requests.get(obj["url"])
                returned_list.append(ConfigExecFile(obj["filename"], r.content))
            elif "path" in obj:
                file_path = project_root + "/" + obj["path"]
                try:
                    fil = open(filePath, "rb")
                    returned_list.append(ConfigExecFile(obj["filename"], fil.read()))
                except:
                    raise Exception("Failed opening file at " + file_path)
        except requests.exceptions.RequestException as e:
            raise FileDownloadError(e)
    return returned_list
