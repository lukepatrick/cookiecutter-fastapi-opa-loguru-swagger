# API Template

This is a [cookiecutter](https://cookiecutter.readthedocs.io/en/1.7.2/) API template that generates the base API skeleton with the following features created

* Standardized API directory structure
* API image ready to build
* Instana metrics, monitoring, and tracing built in
* OPA security hooked in with an example policy
* Setup.py ready to create a wheel file
* Logging out of the box
* Example hello world in place to get started
* Comprehensive docs to start developing
* Tox and pytest testing structures in place

## Creating an API

1. Download [cookicutter](https://cookiecutter.readthedocs.io/en/1.7.2/installation.html)
2. Go to the base of the API repository `/api/`, then run `cookiecutter api-template`
3. cookicutter will prompt the user to fill out each line of information. There is a default/example of each of these values. Enter the proper information for each 
line of information.
4. The api has been created


## Running the API

1. enter the new api directory
2. run `make py-all` to create the virtual env
3. run `make py-run` to start the api locally 
