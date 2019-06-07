#!/usr/bin/python3

import argparse

from lib.config.validate import validateConfigFile


def upCommand(args, unknownArgs):
    print("Fake creating environment")


def downCommand(args, unknownArgs):
    print("Fake turning off environment")


def nukeCommand(args, unknownArgs):
    print("Fake nuking environment")


def runScript(args, unknownArgs, script):
    print('Running script "{}"'.format(script))


def buildCustomCommandParser(subparsers, name, info):
    parser_custom = subparsers.add_parser(name, help=info.get(
        'help'), description=info.get('description'))
    parser_custom.set_defaults(func=lambda args, unknownArgs: runScript(
        args, unknownArgs, info['script']))


def getParser(actions):
    parser = argparse.ArgumentParser(description="ENVY DESCRIPTION TODO")
    subparsers = parser.add_subparsers(dest='subparser_name')
    # Create 'up' parser
    parserUp = subparsers.add_parser('up', help='ENVY UP HELP')
    parserUp.set_defaults(func=upCommand)

    # Create 'down' parser
    parserDown = subparsers.add_parser('down', help='ENVY DOWN HELP')
    parserDown.set_defaults(func=downCommand)

    # Create 'nuke' parser
    parserNuke = subparsers.add_parser('nuke', help='ENVY NUKE HELP')
    parserNuke.set_defaults(func=nukeCommand)

    # Create parsers for 'standard' commands
    if 'build' in actions:
        buildCustomCommandParser(subparsers, 'build', actions['build'])
    if 'lint' in actions:
        buildCustomCommandParser(subparsers, 'lint', actions['lint'])

    # Create parsers for arbitrary custom commands
    if 'custom' in actions:
        for action in actions['custom']:
            buildCustomCommandParser(subparsers, action['name'], action)

    return parser


def main():
    configData = {
        'actions': {
            'build': {
                'script': 'some script',
                'help': 'build the project',
            },
            'lint': {
                'script': 'lint script',
                'help': 'lint the project',
            },
            'custom': [
                {
                    'name': 'customName',
                    'script': 'customScript',
                    'help': 'customHelp',
                    'description': 'customDescription',
                },
            ],
        },
    }

    configData = validateConfigFile(configData)
    parser = getParser(configData['actions'])
    args, unknown = parser.parse_known_args()
    if args.subparser_name:
        args.func(args, unknown)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
