GIT_TAG   = $(shell git describe --tags --always)
DOCKER_BUILD_FLAGS := --network=host
VERSION   ?= ${GIT_TAG}
IMAGE_TAG ?= ${VERSION}

.PHONY: go-clean
go-clean: ## cleans and audits code
	gofmt -s -w .
	golint ./...
	go vet ./...
	go mod tidy

.PHONY: go-test
go-test: ## runs go test and coverage
	go test -cover ./...
