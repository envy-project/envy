import sys
from schema import Schema, SchemaError, Optional

# TODO add schema information for environment stuff
_SCHEMA = Schema(
    {
        "actions": {
            Optional("build"): {
                "script": str,
                "help": str,
                Optional("description"): str,
            },
            Optional("lint"): {
                "script": str,
                "help": str,
                Optional("description"): str,
            },
            Optional("custom"): [
                {"name": str, "script": str, "help": str, Optional("description"): str}
            ],
        }
    }
)


def validateConfigFile(configData):
    try:
        validatedConfigData = _SCHEMA.validate(configData)
    except SchemaError as e:
        sys.exit(e.code)
    return validatedConfigData
