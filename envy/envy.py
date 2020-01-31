#!/usr/bin/python3

import argparse
import time

from envy.lib.config import ENVY_CONFIG, ENVY_CURRENT_RELATIVE_PATH
from envy.lib.state import ENVY_STATE, create_directory_if_not_exists
from envy.lib.docker_manager import ComposeManager, DockerManager
from envy.lib.setup_step import Builder
from envy.lib.io import StepPrinter

STATUS_MSG_NO_CONTAINER = "ENVy has not been initialized for this project. Please run `envy up` to install the ENVy environment."
STATUS_MSG_CONTAINER_STOPPED = (
    "ENVy is not running. Run `envy up` to start the ENVy environment."
)
STATUS_MSG_CONTAINER_READY = "ENVy environment is ready!"


def up_command(_args: argparse.Namespace, _unknow_args: [str]):
    printer = StepPrinter()
    printer.start_step("Finding Docker Container")
    docker_manager = DockerManager()
    printer.end_step()

    if not docker_manager.connection_ok():
        docker_manager.print_connection_err()
        return

    if not ENVY_STATE.get_container_id():
        printer.start_step("No environment detected - Creating ENVy environment")
        docker_manager.create_container()
        create_directory_if_not_exists()
        printer.end_step()

    printer.start_step("Starting Container")
    container = docker_manager.ensure_container()
    container.ensure_running()
    printer.end_step()

    printer.start_step("Performing Build Modules")
    step_builder = Builder(container)
    step_builder.build()
    printer.end_step()

    compose_path = ENVY_CONFIG.get_services_compose_path()
    if compose_path:
        printer.start_step("Starting Sidecar Services")
        ComposeManager(compose_path).up()
        printer.end_step()


def shell_command(_args: argparse.Namespace, _unknown_args: [str]):
    docker_manager = DockerManager()

    if not docker_manager.connection_ok():
        docker_manager.print_connection_err()
        return

    container = docker_manager.get_container()

    if not container:
        print(STATUS_MSG_NO_CONTAINER)
        return

    if not container.is_running():
        print(STATUS_MSG_CONTAINER_STOPPED)
        return

    container.exec("/bin/bash", as_user=True, relpath=str(ENVY_CURRENT_RELATIVE_PATH))


def down_command(_args: argparse.Namespace, _unknown_args: [str]):
    printer = StepPrinter()
    printer.start_step("Connecting to Docker")
    docker_manager = DockerManager()
    printer.end_step()

    if not docker_manager.connection_ok():
        docker_manager.print_connection_err()
        return

    printer.start_step("Finding Docker Container")
    container = docker_manager.get_container()
    printer.end_step()

    if container:
        printer.start_step("Stopping Docker Container")
        container.ensure_stopped()
        printer.end_step()

    compose_path = ENVY_CONFIG.get_services_compose_path()
    if compose_path:
        printer.start_step("Stopping Sidecar Services")
        ComposeManager(compose_path).down()
        printer.end_step()


def nuke_command(_args: argparse.Namespace, _unknown_args: [str]):
    docker_manager = DockerManager()

    if not docker_manager.connection_ok():
        docker_manager.print_connection_err()
        return

    docker_manager.nuke()
    ENVY_STATE.nuke()

    compose_path = ENVY_CONFIG.get_services_compose_path()
    if compose_path:
        ComposeManager(compose_path).nuke()

    print("ENVy environment destroyed")


def status_command(_args: argparse.Namespace, _unknown_args: [str]):
    docker_manager = DockerManager()

    if not docker_manager.connection_ok():
        docker_manager.print_connection_err()
        return

    container = docker_manager.get_container()

    if not container:
        print(STATUS_MSG_NO_CONTAINER)
    elif not container.is_running():
        print(STATUS_MSG_CONTAINER_STOPPED)
    else:
        print("ENVy environment is running!")


def run_script(
    _args: argparse.Namespace,
    unknown_args: [str],
    script: str,
    disable_relpath: bool = False,
):
    docker_manager = DockerManager()

    if not docker_manager.connection_ok():
        docker_manager.print_connection_err()
        return

    container = docker_manager.get_container()

    if not container:
        print(STATUS_MSG_NO_CONTAINER)
    elif not container.is_running():
        print(STATUS_MSG_CONTAINER_STOPPED)
    else:
        command = "{} {}".format(script, " ".join(unknown_args))

        cdto = ENVY_CURRENT_RELATIVE_PATH
        if disable_relpath:
            cdto = None
        container.exec(command, True, cdto)


def build_custom_command_parser(subparsers, name: str, info: {}):
    parser_custom = subparsers.add_parser(name, help=info.get("help"), add_help=False)
    parser_custom.set_defaults(
        func=lambda args, unknown_args: run_script(
            args, unknown_args, info["script"], info["disable_relpath"]
        )
    )


def get_parser(actions: [{}]) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Use ENVy to set up and use your development environment"
    )
    subparsers = parser.add_subparsers(dest="subparser_name")
    # Create 'up' parser
    parser_up = subparsers.add_parser(
        "up", help="Create and start the development environment"
    )
    parser_up.set_defaults(func=up_command)

    # Create 'shell' parser
    parser_shell = subparsers.add_parser(
        "shell", help="Enter a shell in the development environment"
    )
    parser_shell.set_defaults(func=shell_command)

    # Create 'down' parser
    parser_down = subparsers.add_parser("down", help="Stop the development environment")
    parser_down.set_defaults(func=down_command)

    # Create 'nuke' parser
    parser_nuke = subparsers.add_parser(
        "nuke", help="Destroy all ENVy data for this project"
    )
    parser_nuke.set_defaults(func=nuke_command)

    # Create 'status' parser
    parser_status = subparsers.add_parser("status", help="Show ENVy status")
    parser_status.set_defaults(func=status_command)

    # Create parsers for arbitrary custom commands
    for action in actions:
        build_custom_command_parser(subparsers, action["name"], action)

    return parser


def main():
    parser = get_parser(ENVY_CONFIG.get_actions())
    args, unknown = parser.parse_known_args()
    if args.subparser_name:
        args.func(args, unknown)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
