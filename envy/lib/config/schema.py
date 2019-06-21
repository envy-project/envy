import sys

from schema import Schema, SchemaError, Optional, And, Or, Use

_DEFAULT_ENVIRONMENT_BASE = {"image": "ubuntu", "package-manager": "apt"}

_DEFAULT_ENVIRONMENT = {
    "base": _DEFAULT_ENVIRONMENT_BASE,
    "native": [],
    "build-modules": [],
}

_BUILD_MODULE_NOWATCH_TYPES = ["script", "remote"]

_BUILD_MODULE_TRIGGERS = ["once", "always"]

_DEFAULT_BM_TRIGGERS = {"native": [], "files": [], "modules": []}


def __validate_build_module(module: {}) -> bool:
    """ Validates that the given build module contains the appropriate keys given its type

    Arguments:
        module {{}} -- The build module dictionary

    Returns:
        bool -- result
    """
    if module["type"] == "script":
        return "steps" in module
    if module["type"] == "remote":
        return "url" in module or "path" in module
    return False


def __validate_environment_build_modules(environment: {}) -> bool:
    """ Validates that the build modules in the given environment dictionary are valid.
        Verifies that their names are unique, and that they only depend on previously defined modules and native deps

    Arguments:
        environment {{}} -- The environment dictionary

    Returns:
        bool -- Result
    """

    valid_native_names = {dep["recipe"] for dep in environment["native"]}

    seen_module_names = set()

    for module in environment["build-modules"]:
        if module["name"] in seen_module_names:
            print("Module names must be unique")
            return False
        seen_module_names.add(module["name"])

        if isinstance(module["triggers"], list):
            for native_trigger in module["triggers"]["native"]:
                if native_trigger not in valid_native_names:
                    print(
                        "Native triggers can only depend on valid native dependencies"
                    )
                    return False

            for module_trigger in module["triggers"]["modules"]:
                if module_trigger not in seen_module_names:
                    print(
                        "Module triggers can only depend on previously defined modules"
                    )
                    return False
                if module_trigger == module["name"]:
                    print("Module triggers cannot depend on themselves")
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
                Optional("native", default=[]): [
                    {"recipe": str, Optional("version"): Or(str, int, float)}
                ],
                Optional("build-modules", default=[]): [
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
                                    Optional("native", default=[]): [str],
                                    Optional("files", default=[]): [str],
                                    Optional("modules", default=[]): [str],
                                },
                            ),
                            Or("steps", "url", "path", only_one=True): Or([str], str),
                        },
                        __validate_build_module,
                    )
                ],
            },
            __validate_environment_build_modules,
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
