include common.mk
include docker.mk

DOCKER_IMAGE      = api/{{cookiecutter.api_name}}
define DOCKER_RUN_ARGS
-p 8080:8080
endef


VENV_NAME?=venv
VENV_ACTIVATE=. $(VENV_NAME)/bin/activate
PYTHON=${VENV_NAME}/bin/python3

PIP_VERSION  = pip==20.0.2
PY_VERSION   = /usr/local/opt/python@3.7/bin/python3

TEXT_RED     = \033[31m
TEXT_PURPLE  = \033[35m
TEXT_CYAN    = \033[36m
TEXT_DEFAULT = \033[0m ## End Color

# Build
.PHONY: build
build: $(BINS) ## Build the thing


.PHONY: py-all
py-all: py-init py-deps ## python venv init, install deps, and activate venv
    PYTHONPATH=venv ; . venv/bin/activate

.PHONY: py-init
py-init: ## initialize py virtual environment
	@echo "${TEXT_PURPLE}Initializing venv with python: ${TEXT_CYAN}${PY_VERSION}${TEXT_DEFAULT}"
	if [ ! -e "venv/bin/activate_this.py" ] ; then PYTHONPATH=venv ; virtualenv -p $(PY_VERSION) --clear venv ; fi

.PHONY: py-deps
py-deps: ## install python requirements
	@echo "${TEXT_PURPLE}Installing external dependencies using pip: ${TEXT_CYAN}${PIP_VERSION}${TEXT_DEFAULT}"
	PYTHONPATH=venv ; . venv/bin/activate && venv/bin/pip install $(PIP_VERSION) && python --version && venv/bin/pip3 install pip-tools==5.3.1 && venv/bin/pip3 install  -IU -r requirements.txt && if [ "$(ls requirements)" ] ; then venv/bin/pip3 install -IU -r requirements.txt ; fi && venv/bin/pip3 install -IU -r requirements-test.txt

.PHONY: py-deps-clean
py-deps-clean:  ## clears generated requirements files
	@echo "${TEXT_PURPLE}Clearing requirements.txt and requirements-test.txt${TEXT_DEFAULT}"
	true > requirements.txt
	true > requirements-test.txt

.PHONY: py-deps-update
py-deps-update: py-compile ## compiles min requirements and syncs venv with new requirements
	@echo "${TEXT_PURPLE}requirements successfully updated${TEXT_DEFAULT}"

.PHONY: py-compile
py-compile: ## compiles min requirements
	@echo "${TEXT_PURPLE}Compiling min requirements into requirements.txt and requirements-test.txt${TEXT_DEFAULT}"
	pip-compile --rebuild --output-file requirements.txt requirements-min.txt
	pip-compile --rebuild --output-file requirements-test.txt requirements-test-min.txt

.PHONY: py-activate
py-activate: ## activate python venv
	. venv/bin/activate

.PHONY: py-deactivate
py-deactivate: ## deactivate python venv
	deactivate

.PHONY: py-test-unit
py-test-unit: ## run unit tests
	./venv/bin/tox

.PHONY: py-test-integration
py-test-integration: ## run integration tests
	./venv/bin/tox -e integration

.PHONY: py-rm
py-rm: ## remove python venv
	rm -rf venv

CLEANUP = *.pyc

.PHONY: py-clean
py-clean: ## cleanup python compiled files
	find . -name \${CLEANUP} -type f -delete

.PHONY: py-clean-all
py-clean-all: py-deactivate py-rm py-clean ## clean all python/venv

.PHONY: py-lint
py-lint: ## lint all python, limit to ERRORs
	find . -type d \( -path ./venv -o -path ./.tox \) -prune -o -name "*.py" -print0 | xargs -0 ./venv/bin/python -m flake8 && echo "--> No flake8-black action issues found"

.PHONY: py-bandit
py-bandit: ## bandit security scan all python, skipping tests/venv
	find . -type d \( -path ./tests -o -path ./venv -o -path ./.tox \) -prune -o -name "*.py" | xargs ./venv/bin/bandit || true

.PHONY: py-run
py-run: bootstrap ## pipenv run server (if error, show processes on the port)
	PYTHONPATH=venv:. ./venv/bin/python {{cookiecutter.api_name}}/main.py

.PHONY: py-lint-black
py-lint-black: ## lint all python using black (https://github.com/psf/black)
	./venv/bin/black .;

.PHONY: oas
oas: ## Generate openapi spec/swagger doc
	PYTHONPATH=venv:. ./venv/bin/python scripts/export_swagger.py;

#HAS_GOMETALINTER := $(shell command -v gometalinter;)
#HAS_DEP          := $(shell command -v dep;)
HAS_GIT          := $(shell command -v git;)
HAS_DOCKER       := $(shell command -v docker;)
HAS_PYTHON       := $(shell command -v python;)

vendor: ## Preflight checks
ifndef HAS_GIT
        $(error You must install git)
endif
ifndef HAS_DOCKER
        $(error must install docker)
endif
ifndef HAS_PYTHON
        $(error must install python)
endif

.PHONY: bootstrap
bootstrap: vendor
