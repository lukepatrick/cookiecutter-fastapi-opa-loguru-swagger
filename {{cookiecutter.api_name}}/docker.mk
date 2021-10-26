GIT_TAG   = $(shell git describe --tags --always)
DOCKER_BUILD_FLAGS := --network=host
VERSION   ?= ${GIT_TAG}
IMAGE_TAG ?= ${VERSION}

DOCKER_REGISTRY = quay.io

CONTAINER_ID ?= $(shell docker ps | grep '$(DOCKER_REGISTRY)/$(DOCKER_IMAGE):$(IMAGE_TAG)' | cut -d' ' -f1)


.PHONY: docker-build
docker-build: ## Build the container
	docker build -f image/Dockerfile $(DOCKER_BUILD_FLAGS) -t $(DOCKER_REGISTRY)/$(DOCKER_IMAGE):$(IMAGE_TAG) .

# You must be logged into DOCKER_REGISTRY before you can push.
.PHONY: docker-push
docker-push: ## Publish the container
	docker push $(DOCKER_REGISTRY)/$(DOCKER_IMAGE):$(IMAGE_TAG)

.PHONY: docker-security
docker-security: ## docker security scan
	trivy --exit-code 1 --severity CRITICAL image $(DOCKER_REGISTRY)/$(DOCKER_IMAGE):$(IMAGE_TAG)

.PHONY: docker-run
docker-run: ## runs the docker container
	docker run -it --rm $(DOCKER_RUN_ARGS) $(DOCKER_REGISTRY)/$(DOCKER_IMAGE):$(IMAGE_TAG)

.PHONY: docker-stop
docker-stop:  ## stops the running docker container
	docker stop $(CONTAINER_ID)
	