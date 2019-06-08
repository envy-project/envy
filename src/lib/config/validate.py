import sys
from schema import Schema, SchemaError, Optional, Or

# TODO add schema information for environment stuff
_SCHEMA = Schema(
    {
        Optional("environment"): {
            Optional("dependencies"): {
                Optional("python2"): str,
                Optional("python3"): str,
                Optional("node"): str,
                Optional("ruby"): str,
                Optional("native"): [
                    {"recipe": str, "version": Or(str, int, float)},
                ],
            },
        },
        Optional("actions"): [
            {"name": str, "script": str, "help": str, Optional("description"): str},
        ],
    }
)


def validateConfigFile(configData):
    try:
        validatedConfigData = _SCHEMA.validate(configData)
    except SchemaError as e:
        sys.exit(e.code)
    return validatedConfigData
