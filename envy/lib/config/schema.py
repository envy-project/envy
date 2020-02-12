import sys

from typing import Union

from schema import Schema, SchemaError, Optional, And, Or, Use

_DEFAULT_ENVIRONMENT_BASE = {"image": "ubuntu:18.04", "package-manager": "apt"}

_DEFAULT_PROJECT_DIR = "/project"

_DEFAULT_X_FORWARD = False

_DEFAULT_ENVIRONMENT = {
    "base": _DEFAULT_ENVIRONMENT_BASE,
    "x-forward": _DEFAULT_X_FORWARD,
    "project-dir": _DEFAULT_PROJECT_DIR,
    "system-packages": [],
    "setup-steps": [],
}

_STEP_TYPES = ["script", "remote"]

_SIMPLE_TRIGGERS = ["always"]

_DEFAULT_TRIGGERS = {"system-packages": [], "files": [], "steps": []}


def __validate_port_binding(ports: Union[str, int]) -> (str, Optional(str)):
    pair = str(ports).split(":")
    if len(pair) > 2:
        raise SyntaxError("Multiple ':' found: port binding must contain up to 1")
    if len(pair) == 1:
        return (pair[0], None)
    return (pair[0], pair[1])


def __validate_project_dir(project_dir: str) -> bool:
    if not project_dir:
        print("Project directory cannot be empty")
        return False
    if project_dir[0] != "/":
        print("Project directory must have an absolute root path")
        return False
    if len(project_dir) == 1:
        print("Root is not a valid project directory")
        return False

    return True


def __validate_setup_step(step: {}) -> bool:
    """ Validates that the given build step contains the appropriate keys given its type

    Arguments:
        step {{}} -- The build step dictionary

    Returns:
        bool -- result
    """
    if step["type"] == "script":
        return "run" in step
    if step["type"] == "remote":
        return "url" in step or "path" in step
    return False


def __validate_environment_setup_steps(environment: {}) -> bool:
    """ Validates that the build steps in the given environment dictionary are valid.
        Verifies that their names are unique, and that they only depend on previously defined steps and system packages

    Arguments:
        environment {{}} -- The environment dictionary

    Returns:
        bool -- Result
    """

    valid_system_package_names = {
        dep["recipe"] for dep in environment["system-packages"]
    }

    seen_step_names = set()

    for step in environment["setup-steps"]:
        if step["name"] in seen_step_names:
            print("Step names must be unique")
            return False
        seen_step_names.add(step["name"])

        if isinstance(step["triggers"], list):
            for system_package_trigger in step["triggers"]["system-packages"]:
                if system_package_trigger not in valid_system_package_names:
                    print(
                        "system package triggers can only depend on valid system packages"
                    )
                    return False

            for step_trigger in step["triggers"]["steps"]:
                if step_trigger not in seen_step_names:
                    print("Step triggers can only depend on previously defined steps")
                    return False
                if step_trigger == step["name"]:
                    print("Step triggers cannot depend on themselves")
                    return False

    return True


_SCHEMA = Schema(
    {
        Optional("environment", default=_DEFAULT_ENVIRONMENT): And(
            {
                Optional("base", default=_DEFAULT_ENVIRONMENT_BASE): {
                    "image": str,
                    Optional("package-manager"): str,
                },
                Optional("x-forward", default=_DEFAULT_X_FORWARD): bool,
                Optional("project-dir", default=_DEFAULT_PROJECT_DIR): And(
                    str, __validate_project_dir
                ),
                Optional("system-packages", default=[]): [
                    {"recipe": str, Optional("version"): Or(str, int, float)}
                ],
                Optional("setup-steps", default=[]): [
                    And(
                        {
                            "name": str,
                            "type": And(
                                str, Use(str.lower), lambda t: t in _STEP_TYPES
                            ),
                            Optional("label", default=None): str,
                            Optional("triggers", default=_DEFAULT_TRIGGERS): Or(
                                And(
                                    str, Use(str.lower), lambda t: t in _SIMPLE_TRIGGERS
                                ),
                                {
                                    Optional("system-packages", default=[]): [str],
                                    Optional("files", default=[]): [str],
                                    Optional("steps", default=[]): [str],
                                },
                            ),
                            Optional("as_user", default=True): bool,
                            Or("run", "url", "path", only_one=True): Or([str], str),
                        },
                        __validate_setup_step,
                    )
                ],
            },
            __validate_environment_setup_steps,
        ),
        Optional("actions", default=[]): [
            {
                "name": str,
                "script": str,
                "help": str,
                Optional("disable_relpath", default=False): bool,
            }
        ],
        Optional("services", default={}): {Optional("compose-file"): str},
        Optional("network", default={}): Or(
            "host",
            {
                Optional("name", default=None): str,
                Optional("ports", default=None): [Use(__validate_port_binding)],
            },
        ),
    }
)


def validate(raw_data: str) -> {}:
    try:
        return _SCHEMA.validate(raw_data)
    except SchemaError as e:
        sys.exit(e.code)
