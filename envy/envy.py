#!/usr/bin/python3

import argparse
import docker
import dockerpty

from envy.lib.config import ENVY_CONFIG
from envy.lib.state import ENVY_STATE
from envy.lib.docker_helpers.connection_tester import ConnectionTester
from envy.lib.docker_helpers.container_finder import ContainerFinder
from envy.lib.docker_helpers.image_finder import ImageFinder


def up_command(_args, _unknow_args):
    docker_client = docker.from_env()
    connection_tester = ConnectionTester(docker_client)
    container_finder = ContainerFinder(docker_client)
    image_finder = ImageFinder(docker_client)

    if not connection_tester.ok():
        connection_tester.print_err()
        return

    if ENVY_STATE.did_environment_chane():
        print("Detected change in config environment. Re-creating container.")
        container_finder.destroy_container()
        image_finder.destroy_image()

    container_finder.find_or_create_container()
    container_finder.find_and_ensure_running()

    ENVY_STATE.update_environment_hash()
    print("ENVy environment successfully running.")


def shell_command(_args, _unknown_args):
    docker_client = docker.from_env()
    connection_tester = ConnectionTester(docker_client)
    container_finder = ContainerFinder(docker_client)

    if not connection_tester.ok():
        connection_tester.print_err()
        return

    container = container_finder.find_container()

    dockerpty.exec_command(docker_client, container.id, "/bin/bash")


def down_command(_args, _unknown_args):
    docker_client = docker.from_env()
    connection_tester = ConnectionTester(docker_client)
    container_finder = ContainerFinder(docker_client)

    if not connection_tester.ok():
        connection_tester.print_err()
        return

    container_finder.find_and_ensure_stopped()
    print("ENVy environment stopped")


def nuke_command(_args, _unknown_args):
    docker_client = docker.from_env()
    connection_tester = ConnectionTester(docker_client)
    container_finder = ContainerFinder(docker_client)
    image_finder = ImageFinder(docker_client)

    if not connection_tester.ok():
        connection_tester.print_err()
        return

    container_finder.destroy_container()
    image_finder.destroy_image()
    ENVY_STATE.nuke()
    print("ENVy environment destroyed")


def status_command(_args, _unknown_args):
    docker_client = docker.from_env()
    connection_tester = ConnectionTester(docker_client)
    container_finder = ContainerFinder(docker_client)

    if not connection_tester.ok():
        connection_tester.print_err()
        return

    container = container_finder.find_container()

    if container is None:
        print(
            "ENVy has not been initialized for this project. Please run `envy up` to install the ENVy environment."
        )
    elif "running" not in container.status:
        print("ENVy is not running. Run `envy up` to start the ENVy environment.")
    else:
        print("ENVy environment is running!")


def run_script(_args, unknown_args, script):
    docker_client = docker.from_env()
    connection_tester = ConnectionTester(docker_client)
    container_finder = ContainerFinder(docker_client)

    if not connection_tester.ok():
        connection_tester.print_err()
        return

    container = container_finder.find_and_ensure_running()

    command = "/bin/bash -c '{} {}'".format(script, " ".join(unknown_args))
    dockerpty.exec_command(docker_client, container.id, command)


def build_custom_command_parser(subparsers, name, info):
    parser_custom = subparsers.add_parser(
        name, help=info.get("help"), description=info.get("description")
    )
    parser_custom.set_defaults(
        func=lambda args, unknown_args: run_script(args, unknown_args, info["script"])
    )


def get_parser(actions):
    parser = argparse.ArgumentParser(description="ENVY DESCRIPTION TODO")
    subparsers = parser.add_subparsers(dest="subparser_name")
    # Create 'up' parser
    parser_up = subparsers.add_parser("up", help="ENVY UP HELP")
    parser_up.set_defaults(func=up_command)

    # Create 'shell' parser
    parser_shell = subparsers.add_parser("shell", help="ENVY SHELL HELP")
    parser_shell.set_defaults(func=shell_command)

    # Create 'down' parser
    parser_down = subparsers.add_parser("down", help="ENVY DOWN HELP")
    parser_down.set_defaults(func=down_command)

    # Create 'nuke' parser
    parser_nuke = subparsers.add_parser("nuke", help="ENVY NUKE HELP")
    parser_nuke.set_defaults(func=nuke_command)

    # Create 'status' parser
    parser_status = subparsers.add_parser("status", help="ENVY STATUS HELP")
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
