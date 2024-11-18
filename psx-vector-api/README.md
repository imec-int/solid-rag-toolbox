# Python FastAPI Template

This documentation provides an overview of the features included in this template.

## Dev Container

The template project includes a dev container configuration that allows you to develop and run the project in a consistent and isolated environment. The dev container is defined using Docker and includes all the necessary dependencies and tools required for development. Adjust if needed per project's requirements.

## Taskfile

The template project utilizes a Taskfile to define and automate common development tasks. The Taskfile is a simple and flexible task runner that allows you to define tasks using YAML syntax. It provides a convenient way to run commands, scripts, and other tasks related to your project.

Docs for Taskfile can be found [here](https://taskfile.dev/).

## Poetry

The template project utilizes Poetry as a dependency management and packaging tool for Python projects. Poetry simplifies the process of managing project dependencies and ensures consistent and reproducible builds.

Please note that if you use the devcontainer, Poetry and Taskfile are not required to install locally.

Docs for Poetry can be found [here](https://python-poetry.org/docs/).

## Pkl

In this template, Pkl-lang files are used for configuring the application's config and its data model.
Docs for Pkl can be found [here](https://pkl-lang.org/).

---

Read more about [development](docs/development.md)
