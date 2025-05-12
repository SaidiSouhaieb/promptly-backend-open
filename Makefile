PROJECT_NAME=promptly
DOCKERFILE_PATH=./docker/Dockerfile
BUILD_CONTEXT=..
DOCKER_COMPOSE_PATH=docker-compose.yml
DOCKER_COMPOSE= docker-compose  --env-file=.env

build:
	${DOCKER_COMPOSE} -f ${DOCKER_COMPOSE_PATH} build

up:
	${DOCKER_COMPOSE} -f ${DOCKER_COMPOSE_PATH} up -d

down:
	${DOCKER_COMPOSE} -f ${DOCKER_COMPOSE_PATH} down

clean:
	${DOCKER_COMPOSE} -f ${DOCKER_COMPOSE_PATH} down --rmi all

start: build up

rebuild: clean start

logs:
	${DOCKER_COMPOSE} -f ${DOCKER_COMPOSE_PATH} logs -f
