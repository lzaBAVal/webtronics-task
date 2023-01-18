THIS_FILE := $(lastword $(MAKEFILE_LIST))
.PHONY: help build up start down stop restart logs ps build-test run-test build-dev run-dev down-dev restart-dev

help:
		echo "help build up start down stop restart logs ps build-test run-test build-dev run-dev down-dev restart-dev"
build:
		docker build -t webtronics-task-app -f docker/Dockerfile . $(c)
up:
		docker-compose -f docker/docker-compose.yml up -d $(c)
start:
		docker-compose -f docker-compose.yml start $(c)
down:
		docker-compose -f docker/docker-compose.yml down $(c)
stop:
		docker-compose -f docker-compose.yml stop $(c)
restart:
		docker-compose -f docker-compose.yml stop $(c)
		docker-compose -f docker-compose.yml up -d $(c)
logs:
		docker-compose -f docker-compose.yml logs --tail=100 -f $(c)
ps:
		docker-compose -f docker-compose.yml ps
build-test:
		docker build -t test-webtronics-task-app -f docker/Dockerfile-test .
up-test:
		docker-compose -f docker/docker-compose-test.yml up --abort-on-container-exit $(c) && docker-compose -f docker/docker-compose-test.yml down
down-test:
		docker-compose -f docker/docker-compose-test.yml down
build-dev:
		docker-compose -f docker/docker-compose-dev.yml build --no-cache
up-dev:
		docker-compose -f docker/docker-compose-dev.yml up -d
down-dev:
		docker-compose -f docker/docker-compose-dev.yml down
restart-dev:
		docker-compose -f docker-compose-dev.yml stop $(c)
		docker-compose -f docker-compose-dev.yml up -d $(c)
down-all:
		docker-compose -f docker/docker-compose-test.yml down && \
		docker-compose -f docker/docker-compose-dev.yml down && \
		docker-compose -f docker/docker-compose.yml down
