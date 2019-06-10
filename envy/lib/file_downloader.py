import requests

class ConfigExecFile:
    def __init__(self, filename, byt):
        self.filename = filename
        self.bytes = byt


class FileDownloadError(Exception):
    def __init__(self, requestsError):
        super(FileDownloadError, self).__init__()
        self.requestsError = requestsError

def resolveFiles(fileObjects):
    """ Turn file objects from the config into "real" objects with Byte strings. Currently only supports URL format
        Args:
            fileObjects (list<dict>): fileObjects from the config
        Returns:
            list<ConfigExecFile>: List of executable files to run in the image
        Raises:
            FileDownloadError: When a file fails to download for some reason. Contains the Requests error.
    """
    if not fileObjects:
        return None
    returnedList = []
    for obj in fileObjects:
        try:
            r = requests.get(obj["url"])
            returnedList.append(ConfigExecFile(obj["filename"], r.content))
        except requests.exceptions.RequestException as e:
            raise FileDownloadError(e)
    return returnedList
