# Linting and Formatting
Linting in Python is necessary due to the many runtime exceptions that it can through. Running the code through a linter will catch many of these runtime exceptions before they become a problem. Combining linting with formatting will help ensure the standardization in the code's appearance and remove unnecessary lines of code such as unused import statements

## Std library
[flake8-black](https://github.com/peterjc/flake8-black)

## Configuration files
`pytest.ini`
## What this library provides
Flake8-black is an extension of the [flake8](https://gitlab.com/pycqa/flake8) tool where flake8-black will check to ensure the user ran their code through the [black](https://github.com/psf/black) formatter. If the user fails to run black on their code and flake8-black detects the code would change with black, it will fail the linting. This is done to enforce users run black against their code

## Usage
The linting and formatting tool will be run in CICD in the API before it is allowed to be merged in. To ensure the code passes CICD, it is recommended the user run `make py-lint` before submitting an MR to detect issues in the code
