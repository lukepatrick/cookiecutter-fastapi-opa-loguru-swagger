# Testing

## Developing tests

See [test standards](./api_standards/testing.md) for mor information

## Running tests

Tests can be run a couple of ways.

### Run unit tests with tox

`$ tox`

or 

`$ make py-test-unit`


### Run unit tests with pytest

`python -m pytest --maxfail=2 -v --cov=<name of src dir> --no-cov-on-fail --nf --continue-on-collection-errors --tb=long --showlocals tests/unit`

### Run integration tests with tox

`$ tox -e integration`

or 

`$ make py-test-integration`


### Run integration tests with pytest

`python -m pytest --maxfail=2 -v --cov=<name of src dir> --no-cov-on-fail --nf --continue-on-collection-errors --tb=long --showlocals tests/integration`

