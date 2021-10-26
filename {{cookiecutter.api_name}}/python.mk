VENV_NAME?=venv
VENV_ACTIVATE=. $(VENV_NAME)/bin/activate
PYTHON=${VENV_NAME}/bin/python3

PY_VERSION  = 3.7
PIP_VERSION = --upgrade pip
# PIP_VERSION= pip==20.0.2

.PHONY: py-all
py-all: py-init py-deps ## python venv init, install deps, and activate venv
	PYTHONPATH=venv ; . venv/bin/activate; python --version ; pip --version

.PHONY: py-init
py-init: ## initialize py virtual environment
	if [ ! -e "venv/bin/activate_this.py" ] ; then PYTHONPATH=venv ; virtualenv -p python$(PY_VERSION) --clear venv ; fi

.PHONY: py-deps
py-deps: ## install python requirements
	PYTHONPATH=venv ; . venv/bin/activate && venv/bin/pip install $(PIP_VERSION) && python --version && venv/bin/pip install -IU -r requirements.txt && if [ "$(ls requirements)" ] ; then venv/bin/pip install -IU -r requirements/* ; fi && venv/bin/pip install -IU -r requirements-test.txt

.PHONY: py-compile
py-compile: ## compiles all requirements
	PYTHONPATH=venv ; . venv/bin/activate && pip-compile --rebuild --output-file requirements.txt requirements-min.txt

.PHONY: py-rm
py-rm: ## remove python venv
	rm -rf venv

.PHONY: py-activate
py-activate: ## activate python venv
	. venv/bin/activate

.PHONY: py-deactivate
py-deactivate: ## deactivate python venv
	deactivate

.PHONY: py-test-unit
py-test-unit: ## run unit tests
	nose2 -v -c noseunit.cfg

.PHONY: py-test-integration
py-test-integration: ## run integration tests
	nose2 -v -c noseint.cfg

CLEANUP = *.pyc

.PHONY: py-clean
py-clean: ## cleanup python compiled files
	find . -name \${CLEANUP} -type f -delete

.PHONY: py-clean-all
py-clean-all: py-deactivate py-rm py-clean ## clean all python/venv

.PHONY: py-lint
py-lint: ## lint all python, limit to ERRORs
	find . -path ./venv -prune -o -name "*.py" -print0 | xargs -0 python3 -m pylint -E --rcfile=.pylintrc && echo "--> No pylint action issues found"

.PHONY: py-yamllint
py-yamllint: ## lint all yaml, exit 0 limit to ERRORs
	find . -path ./venv -prune -o -name "*.yaml" -print0 | xargs -0 python3 -m yamllint -c .yamllint && echo "--> No yamllint action issues found"

.PHONY: py-bandit
py-bandit: ## bandit security scan all python, skipping tests/venv
	find . -type d \( -path ./tests -o -path ./venv \) -prune -o -name "*.py" | xargs bandit || true