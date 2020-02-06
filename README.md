ENVy
====

ENVy is the easy way to build development environments. It allows maintainers to specify exactly the environment that contributors should be using, not just for packages for the language in use, but native system packages as well. No more following pages-long contributing guides, or trying to figure out the strange problem that only one user has, just run `envy up` and contributors can start writing code. It's like a virtualenv, but for **everything**!

Check out our [main website](https://envy-project.github.io/) for more details on ENVy.

Installing ENVY
---

**Prerequisites**: You should have Docker installed and running (i.e. `docker ps` doesn't give you an error), as well as `docker-compose`, needed for some projects.

You can install ENVy in a few different ways:

*pip (recommended)*:
   - The recommended installation method is to use Pip: `pip3 install envy-project`.

*from release (or master)*:
   - Download a tar.gz release from [ENVy's Github release page](https://github.com/envy-project/envy/releases).
   - Extract the archive (`tar -xzvf envy-*.tgz`)
   - Install the package (`sudo setup.py install`)

**Special Instructions for Mac OS X**:
   - Install [Docker for Mac](https://docs.docker.com/docker-for-mac/install/).
   - If your project uses X-forwarding:
     1. Install [XQuartz](https://www.xquartz.org/).
     2. Enable the "Allow connections from network clients" setting under XQuartz's security tab.
     3. (re)Start XQuartz. XQuartz must be running for X-forwarding to work.

Using ENVy as a contributor
---

ENVy is a very simple tool to use. You can see all available commands by running `envy --help`. When you're working with a project, this help text will also contain all of the project-specific commands you can use (build, lint, etc.)

ENVy itself also defines a few commands:

- `envy up`: Create a development environment

When run inside of a project directory, this will create a development environment according to the maintainer's specifications. You will see progress output as the process continues. It will mount the project directory inside of the environment. You can leave this container running as long as you'd like - it consumes little to no resources.

```
~ $ cd golang-hello-world
golang-hello-world $ envy up
Detected change in config environment.
Creating ENVy environment image.
Creating ENVy container
ENVy environment is ready!
```

- `envy down`: Pause a development environment

When run inside of a project directory, this will pause the development environment without deleting any data. You may want to run this when you're finished working on a project for a little while.


```
~ $ golang-hello-world $ envy down
ENVy environment stopped.
```

- `envy nuke`: Delete a development environment

When run inside of a project directory, this will remove the environment created by ENVy. This will not affect the project directory itself - you will not lose any work. This frees up storage space on your host computer. Note that depending on the project configuration, this could delete temporary data - such as a database in use for development.

```
~ $ golang-hello-world $ envy nuke
ENVy environment destroyed.
```

Setting up your projects to use ENVy
---
Creating Envyfiles is easy! Please follow the [Maintainer's Guide](https://envy-project.github.io/maintainer-guide.html), or take a look at the [Envyfile Reference](https://envy-project.github.io/envyfile-reference.html). You may also find the [examples repository](https://github.com/envy-project/examples) to be a handy resource.

And, once you're done, please let us know how it went! If you've built an Envyfile for a new language or project type, consider opening an issue or a PR in our [examples repository](https://github.com/envy-project/examples) to help others out.


Frequently Asked Questions
---

- **Q: How does ENVy work?**
  - ENVy helps projects by making it very easy for projects to use Docker for environment setup. Most aspects of managing Docker container lifecycles are handled transparently, without the need for project maintainers to think about what needs to happen at each step.
- **Q: How can I support the project?**
  - The best way to help ENVy is to _use it_! With your help, we can learn how projects use ENVy in the real world, and make your use cases easier for you to configure. Please file [issues](https://github.com/envy-project/envy/issues) for any problems you encounter!
