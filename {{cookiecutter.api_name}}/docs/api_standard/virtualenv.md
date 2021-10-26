# VirtualEnv
In order to keep the system's Python libraries sanitized, it is important to separate the necessary imports into virtual environments
# Std Library
[virtualenv](https://docs.python.org/3/tutorial/venv.html)

## Creating virtual environment
Run

`$ make py-all` 

in order to construct a `venv` directory with all of the necessary requirements for the project. From this directory, the user can source the Python interpreter with 

`$ source  ./venv/bin/active`

to use that specific python and its site-packages