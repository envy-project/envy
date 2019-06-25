ENVy
====

ENVy is an environment manager that allows developers on a project to get easily set up, both by managing dependency installation and by making common workflows easily discoverable.

## Config Docs
The ENVy config file contains all the information ENVy uses to manage your project. At the root of your project directory create a YAML file called `.envyfile`.

The top level of the file contains 3 keys: environment, actions, and services.

## Environment:
### base:
This contains the information for the base system to be running. If not specified, ENVy will use a standard Ubuntu system

    image: <The docker image that the environment should be built off of>

### system-packages:
The list of packages that your project needs that would come from a package manager (ex. `apt` in Ubuntu)

Each entry in the list will should be an object of the following form:

    package: <The name of the package>
    version: <The string repesenting a fixed version of the package>

### setup-steps:
The list of steps required to take the base system with the system packages and install the rest of the dependencies. This is where you'd put actions like installing python depenendencies or seeding a database.

    name: <The human-readable name given for this build step>
    type: <Either script or remote>
    triggers: <The trigger for this action: see below>

There are two kinds of steps.

A `script` type setup step is used for executing a list of shell commands inside the environment. This step has an additional `run` key:

    run: <A list of shell commands to execute>

A `remote` type setup step is used for executing a shell script that can be pulled from a remote location, such as installing `meteor`. This step type has an additional `url` key:

    url: <The url to download the bash script from>

#### Triggers
The `triggers` key is optional, and controls how often the command is re-executed on `envy up`. By default, the command will only be run once per environment: it will only run again if the user executes `envy nuke`.

A trigger can be defined as `once`. This is used for commands that should only ever be run once for the entire lifetime of the project. An example would be the seeding of a database: it would write to a file in the project directory to create the initial database, but shouldn't be re-run since envy will never modify files inside the project.

A trigger can be defined as `always`. This command will be run on every invocation of `envy up`. This would be used for commands that need to be kept up to date, such as a dependency installation that must always be running the newest version.

Alternatively, a trigger can be given an object detailing more complex trigger mechanisms, like so:

    triggers:
      system-packages: <A list of previously-defined system packages this step should trigger on. This will cause a re-run if the version of that package is changed>
      files: <A list of files within the project's directory. This will cause a re-run when the contents of any of those files change.>
      steps: <A list of previously-defined setup-steps. This will cause a re-run when any of the listed steps are themselves triggered for a re-run>

## Actions:
A list of common workflows for the project. These would include anything from compiling a C++ application to linting a python project to starting up a web server. Anything that a developer would commonly do can be placed as an action, to be found with `envy --help`. Each action has a structure as follows:

    name: <The sub-command name used on when invoking envy>
    script: <The bash script executed in the environment for this action>
    help: <The help message shown next to the command in envy --help>

## Services
For projects that have sidecar services (such as a separate database) that use docker-compose, this key allows envy to manage those. Give envy a docker-compose file as so:

    compose-file: <Name of docker-compose file in the project>

On `envy up` the sidecar service will be started, and `envy down` will stop the sidecar.
