import sys

from schema import Schema, SchemaError, Optional, Or

_SCHEMA = Schema(
    {
        Optional("environment", default={}): {
            Optional("dependencies", default={}): {
                Optional("python2", default="requirements.txt"): str,
                Optional("python3", default="Pipfile"): str,
                Optional("node", default="package.json"): str,
                Optional("ruby", default="gemfile"): str,
                Optional("native", default=[]): [
                    {"recipe": str, "version": Or(str, int, float)}
                ],
                Optional("executables", default=[]): [
                    {"filename": str, "url": str}
                ],
            }
        },
        Optional("actions"): [
            {"name": str, "script": str, "help": str, Optional("description"): str}
        ],
    }
)


def validateSchema(rawData):
    try:
        return _SCHEMA.validate(rawData)
    except SchemaError as e:
        sys.exit(e.code)  # TODO shouldn't exit here
