ENVy
====

ENVy is an environment manager that allows developers to get easily set up with a project, both by managing dependency installation and by making common workflows easily discoverable.

## Config Docs
The ENVy config file contains all the information ENVy uses to manage your project. At the root of your project directory create a YAML file called `.envyfile`. Check out some example envyfiles [here](https://TODO.com).

The top level of the file contains 3 keys: environment, actions, and services.

## Environment:
### base:
This contains the information for the base system to be running. If not specified, ENVy will use Ubuntu 18

    image: <The docker image that the environment should be built off of>

(Note: we currently only support Ubuntu images)
This might look like:

    base:
      image: ubuntu:18.04

### system-packages:
The list of packages that your project needs that would come from a package manager (ex. `apt` in Ubuntu)

Each entry in the list should be an object of the following form:

    package: <The name of the package>
    version: <Optional: A version string to pin this package to>

An example config might look like

    system-packages:
    - package: curl
      version: 7.65.0
    - package: wget
    - package: python3

### setup-steps:
The list of steps required to take the base system with the system packages and install the rest of the dependencies. This is where you'd put actions like installing python dependencies or seeding a database.

    name: <The human-readable name given for this build step>
    type: <Either script or remote>
    triggers: <The (optional) trigger for this action: see below>

There are two kinds of steps.

A `script` type setup step is used for executing a list of shell commands inside the environment. This step has an additional `run` key:

    run: <One or more shell commands to execute. Ex: 'npm run install'>

A `remote` type setup step is used for executing a shell script that can be pulled from a remote location, such as installing `meteor`. This step type has an additional `url` key:

    url: <The url to download the bash script from>

#### Triggers
The `triggers` key is optional, and controls how often the command is re-executed on `envy up`. By default, the command will only be run once per environment: it will only run again if the user executes `envy nuke`.

A trigger can be defined as `always`. This command will be run on every invocation of `envy up`.

Alternatively, a trigger can be given an object detailing more complex trigger mechanisms, like so:

    triggers:
      system-packages: <A list of previously-defined system packages this step should trigger on. This will cause a re-run if the version of that package is changed>
      files: <A list of files within the project's directory. This will cause a re-run when the contents of any of those files change. Ex: 'Pipfile' for a python dependencies step>
      steps: <A list of previously-defined setup-steps. This will cause a re-run when any of the listed steps are themselves triggered for a re-run>

An example trigger set might look like:

    triggers:
      files:
        - Pipfile
        - Pipfile.lock
      steps:
        - pipenv

Here, the setup step would run the first time in a clean environment, and then would re-trigger on `envy up` if Pipfile or Pipfile.lock changed, *or* if a previous step called `pipenv` was run.

## Actions:
A list of common workflows for the project. These would include anything from compiling a C++ application to linting a python project to starting up a web server. Anything that a developer would commonly do can be placed as an action, to be found with `envy --help`. Each action has a structure as follows:

    name: <The sub-command name used on when invoking envy>
    script: <The bash script executed in the environment for this action>
    help: <The help message shown next to the command in envy --help>

One such action could be linting javascript code:

    actions:
    - name: lint
      script: 'eslint .'
      help: 'lint the project'

## Services
ENVy can manage sidecar services for you using docker-compose. Point envy to your docker-compose file like so:

    compose-file: <Name of docker-compose file in the project>

The sidecar services will be started on `envy up`, and stopped on `envy down`
