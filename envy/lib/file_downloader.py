import requests
from envy.lib.config.file import findProjectRoot


class ConfigExecFile:
    def __init__(self, filename, byt):
        self.filename = filename
        self.bytes = byt


class FileDownloadError(Exception):
    def __init__(self, requestsError):
        super(FileDownloadError, self).__init__()
        self.requestsError = requestsError


def resolveFiles(fileObjects):
    """ Turn file objects from the config into "real" objects with Byte strings.
        Support URL and path formats
        Args:
            fileObjects (list<dict>): fileObjects from the config
        Returns:
            list<ConfigExecFile>: List of executable files to run in the image
        Raises:
            FileDownloadError: When a file fails to download for some reason. Contains the Requests error.
    """
    if not fileObjects:
        return None
    projectRoot = findProjectRoot()
    returnedList = []
    for obj in fileObjects:
        try:
            if "url" in obj:
                r = requests.get(obj["url"])
                returnedList.append(ConfigExecFile(obj["filename"], r.content))
            elif "path" in obj:
                filePath = projectRoot + "/" + obj["path"]
                try:
                    fil = open(filePath, "rb")
                    returnedList.append(ConfigExecFile(obj["filename"], fil.read()))
                except:
                    raise Exception("Failed opening file at " + filePath)
        except requests.exceptions.RequestException as e:
            raise FileDownloadError(e)
    return returnedList
