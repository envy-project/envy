import sys

from schema import Schema, SchemaError, Optional, And, Or, Use

_DEFAULT_ENVIRONMENT_BASE = {"image": "ubuntu:18.04", "package-manager": "apt"}

_DEFAULT_ENVIRONMENT = {
    "base": _DEFAULT_ENVIRONMENT_BASE,
    "system-packages": [],
    "setup-steps": [],
}

_BUILD_MODULE_NOWATCH_TYPES = ["script", "remote"]

_BUILD_MODULE_TRIGGERS = ["once", "always"]

_DEFAULT_BM_TRIGGERS = {"system-packages": [], "files": [], "steps": []}


def __validate_setup_step(step: {}) -> bool:
    """ Validates that the given build step contains the appropriate keys given its type

    Arguments:
        step {{}} -- The build step dictionary

    Returns:
        bool -- result
    """
    if step["type"] == "script":
        return "steps" in step
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
                Optional("system-packages", default=[]): [
                    {"recipe": str, Optional("version"): Or(str, int, float)}
                ],
                Optional("setup-steps", default=[]): [
                    And(
                        {
                            "name": str,
                            "type": And(
                                str,
                                Use(str.lower),
                                lambda t: t in _BUILD_MODULE_NOWATCH_TYPES,
                            ),
                            Optional("triggers", default=_DEFAULT_BM_TRIGGERS): Or(
                                And(
                                    str,
                                    Use(str.lower),
                                    lambda t: t in _BUILD_MODULE_TRIGGERS,
                                ),
                                {
                                    Optional("system-packages", default=[]): [str],
                                    Optional("files", default=[]): [str],
                                    Optional("steps", default=[]): [str],
                                },
                            ),
                            Or("steps", "url", "path", only_one=True): Or([str], str),
                        },
                        __validate_setup_step,
                    )
                ],
            },
            __validate_environment_setup_steps,
        ),
        Optional("actions", default=[]): [
            {"name": str, "script": str, "help": str, Optional("description"): str}
        ],
        Optional("services", default={}): {Optional("compose-file"): str},
    }
)


def validate(raw_data: str) -> {}:
    try:
        return _SCHEMA.validate(raw_data)
    except SchemaError as e:
        sys.exit(e.code)
