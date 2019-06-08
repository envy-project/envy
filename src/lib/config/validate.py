import sys
from schema import Schema, SchemaError, Optional

# TODO add schema information for environment stuff
_SCHEMA = Schema(
    {
        Optional("actions"): [
            {"name": str, "script": str, "help": str, Optional("description"): str}
        ]
    }
)


def validateConfigFile(configData):
    try:
        validatedConfigData = _SCHEMA.validate(configData)
    except SchemaError as e:
        sys.exit(e.code)
    return validatedConfigData
