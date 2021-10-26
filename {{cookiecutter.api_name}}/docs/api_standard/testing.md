# Testing
Testing is one of the most essential components to developing an API. Whether the tests are created through test driven development, or they were written after the code, it is important to develop tests

## Std Libraries
[pytest](https://docs.pytest.org/en/stable/) - The testing framework to use.

[tox](https://tox.readthedocs.io/en/latest/) - Tox is the test runner. The value that derives from tox is its ability to create clean environments, as well as test multiple Python versions.

## Configuration files
`tox.ini`

`pytest.ini`
## Adding tests
**unit tests** - Unit tests are tests that do not invoke external systems. They only focus on testing the API's code. When testing code that makes external connections, those calls need to be [mocked](https://medium.com/@bfortuner/python-unit-testing-with-pytest-and-mock-197499c4623c). Ensure call unit tests are in the `tests/unit` directory.

**integration tests** - Integration tests are autological. They tests the code against the external systems it uses. Ensure call unit tests are in the `tests/integration` directory. 

---
> **_NOTE:_** The `__init__` files of both the unit and integration directory contains the code necessary to source the API source code when running tests from the command line.
---

## Running tests
Tests can be run by using three methods, make, tox, pytest.

### Make

The Makefile runs tests using to (see below for the direct implementation)

For **unit** tests, run 

`$ make py-test-unit`

For **integration** tests, run

`$ make py-test-integration`

### Tox
To run the tox for **unit** tests, run the following command at the root level of the project

`$ tox`

To run it for **integration** tests, run the following command at the root level of the project

`$ tox -e integration`

### Pytest

To run pytest for **unit** tests, run the following command at the root level of the project

`$ python -m pytest --maxfail=2 -v --cov=<name of src dir> --no-cov-on-fail --nf --continue-on-collection-errors --tb=long --showlocals tests/unit`

For **integration** tests

`$ python -m pytest --maxfail=2 -v --cov=<name of src dir> --no-cov-on-fail --nf --continue-on-collection-errors --tb=long --showlocals tests/integration`

---
>**Note:** You can run tests at an individual test file level, just point the command to the file you want to run.
---