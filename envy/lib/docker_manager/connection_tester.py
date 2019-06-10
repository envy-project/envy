import docker
from requests.exceptions import ConnectionError as RequestsConnectionError


class ConnectionTester:
    def __init__(self, dockerClient):
        self.client = dockerClient
        self.result = False
        self.message = ""

        self.__test()

    def __test(self):
        try:
            if self.client.ping():
                self.result = True
            else:
                self.result = False
                self.message = "Docker daemon is unavailable"
        except docker.errors.APIError as e:
            if e.status_code == 502:
                self.message = "Docker daemon is unavailable (502). Is it starting up?"
            elif e.status_code == 403:
                self.message = "Connection denied (403). Do you have permission to connect to docker?"
            elif e.status_code == 401:
                self.message = "Connection denied (401). Do you have permission to connect to docker?"
            else:
                self.message = "HTTP error (e.status_code)."
        except RequestsConnectionError as e:
            self.message = "Connection refused. Is docker running?"
        except Exception as e:  # pylint: disable=W0703
            self.message = str(e)

    def ok(self):
        return self.result

    def reason(self):
        return self.message

    def print_err(self):
        print(self.message)
