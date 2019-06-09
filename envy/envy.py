#!/usr/bin/python3

import argparse
import docker
import dockerpty

from envy.lib.config import ENVY_CONFIG
from envy.lib.state import ENVY_STATE
from envy.lib.docker_helpers.container_finder import ContainerFinder
from envy.lib.docker_helpers.image_finder import ImageFinder


def upCommand(_args, _unknownArgs):
    dockerClient = docker.from_env()
    containerFinder = ContainerFinder(dockerClient)

    if ENVY_STATE.didEnvironmentChange():
        print("Detected change in config environment. Re-creating container.")
        containerFinder.destroyContainer()
        # TODO this creates the container if not found, then immediately destroys it
        # TODO this does not remove the image

    containerFinder.findOrCreateContainer()
    containerFinder.findAndEnsureRunning()

    ENVY_STATE.updateEnvironmentHash()
    print("ENVy environment successfully running.")


def downCommand(_args, _unknownArgs):
    dockerClient = docker.from_env()
    containerFinder = ContainerFinder(dockerClient)

    containerFinder.findAndEnsureStopped()
    print("ENVy environment stopped")


def nukeCommand(_args, _unknownArgs):
    dockerClient = docker.from_env()
    containerFinder = ContainerFinder(dockerClient)
    imageFinder = ImageFinder(dockerClient)

    containerFinder.destroyContainer()
    imageFinder.destroyImage()
    ENVY_STATE.nuke()
    print("ENVy environment destroyed")


def runScript(_args, unknownArgs, script):
    dockerClient = docker.from_env()
    containerFinder = ContainerFinder(dockerClient)
    container = containerFinder.findAndEnsureRunning()

    command = "{} {}".format(script, " ".join(unknownArgs))
    dockerpty.exec_command(dockerClient, container.id, command)


def buildCustomCommandParser(subparsers, name, info):
    parser_custom = subparsers.add_parser(
        name, help=info.get("help"), description=info.get("description")
    )
    parser_custom.set_defaults(
        func=lambda args, unknownArgs: runScript(args, unknownArgs, info["script"])
    )


def getParser(actions):
    parser = argparse.ArgumentParser(description="ENVY DESCRIPTION TODO")
    subparsers = parser.add_subparsers(dest="subparser_name")
    # Create 'up' parser
    parserUp = subparsers.add_parser("up", help="ENVY UP HELP")
    parserUp.set_defaults(func=upCommand)

    # Create 'down' parser
    parserDown = subparsers.add_parser("down", help="ENVY DOWN HELP")
    parserDown.set_defaults(func=downCommand)

    # Create 'nuke' parser
    parserNuke = subparsers.add_parser("nuke", help="ENVY NUKE HELP")
    parserNuke.set_defaults(func=nukeCommand)

    # Create parsers for arbitrary custom commands
    for action in actions:
        buildCustomCommandParser(subparsers, action["name"], action)

    return parser


def main():
    parser = getParser(ENVY_CONFIG.getActions())
    args, unknown = parser.parse_known_args()
    if args.subparser_name:
        args.func(args, unknown)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
