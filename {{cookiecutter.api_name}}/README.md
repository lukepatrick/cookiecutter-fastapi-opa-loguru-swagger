# API Template

## How to use

To build a new template, first install the cookiecutter tool.

`pip install cookiecutter`

Run the tool to generate a new API

`cookiecutter api-template`

It will then prompt the user for information to generate the API skeleton

## Features

The API template will generate the following features

* Standardized API skeleton and dependencies
* API security using Open Policy Agent built in
* Logger already started
* A working API with examples to immediately begin development
* Base Dockerfile created
* Testing ready to go

# Developing a API
[API Standard Libraries](./docs/api_standard.md) - The standard external libraries to use throughout the app

[API Structure](./docs/api_structure.md) - Understanding the API skeleton structure

[API Security](./docs/api_security.md) - Securing the API with JWT and OPA

[Configuration](./docs/configuration.md) - How to configure the app with a `.env` file or env variables

[Running API](./docs/running_api.md) - Deep dive into how to start the app and what happens

[Testing](./docs/testing.md) - Developing and running tests

[Building Container](./docs/building_container.md) - How to develop and build the container
