import hashlib
import json

from .config import ENVY_CONFIG


def hashFullConfig():
    return hashlib.md5(json.dumps(ENVY_CONFIG).encode("utf-8")).hexdigest()


def hashEnvironmentConfig():
    return hashlib.md5(
        json.dumps(ENVY_CONFIG["environment"]).encode("utf-8")
    ).hexdigest()
