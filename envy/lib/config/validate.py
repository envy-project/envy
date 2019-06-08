import sys
from schema import Schema, SchemaError, Optional, Or

# TODO add schema information for environment stuff
_SCHEMA = Schema(
    {
        Optional("environment", default={}): {
            Optional("dependencies", default={}): {
                Optional("python2", default="requirements.txt"): str,
                Optional("python3", default="Pipfile"): str,
                Optional("node", default="package.json"): str,
                Optional("ruby", default="gemfile"): str,
                Optional("native", default=[]): [{"recipe": str, "version": Or(str, int, float)}],
            }
        },
        Optional("actions"): [
            {"name": str, "script": str, "help": str, Optional("description"): str}
        ],
    }
)


def validateConfigFile(configData):
    try:
        validatedConfigData = _SCHEMA.validate(configData)
    except SchemaError as e:
        sys.exit(e.code)
    return validatedConfigData
