import hashlib
import json


def hashFullConfig(config):
    return hashlib.md5(json.dumps(config).encode("utf-8")).hexdigest()


def hashEnvironmentConfig(config):
    return hashlib.md5(json.dumps(config["environment"]).encode("utf-8")).hexdigest()
