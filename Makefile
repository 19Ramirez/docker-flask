# Makefile for Tecticom/Docker-Flask project (Windows Version)

# Variables alineadas con tu repositorio actual
IMAGE_NAME = ghcr.io/19ramirez/docker-flask:1.0.0
STACK_FILE = stack.yml

# GNU Make en Windows lee variables de entorno directamente usando $(VAR)
VPS_USER = $(VPS_USER)
VPS_HOST = $(VPS_HOST)
VPS_SSH_PORT = $(VPS_SSH_PORT)

# Default target
.PHONY: all
all: help

# Help
.PHONY: help
help:
	@echo Available targets:
	@echo   build      Build Docker image locally
	@echo   push       Push image to GitHub Container Registry
	@echo   deploy     Deploy stack to VPS (scp stack.yml)
	@echo   clean      Remove local Docker images

# Build Docker image
.PHONY: build
build:
	docker build -t $(IMAGE_NAME) .

# Push image to GHCR (Usando sintaxis limpia para pipes en CMD de Windows)
.PHONY: push
push:
	@echo | set /p="$(GHCR_PAT)" | docker login ghcr.io -u $(GITHUB_ACTOR) --password-stdin
	docker push $(IMAGE_NAME)

# Deploy to VPS (Alineado a la carpeta /landinga y al stack /borrar)
.PHONY: deploy
deploy:
	@echo Copying $(STACK_FILE) to VPS...
	@echo Ejecutando comandos en servidor remoto...
	sshpass -p "$(VPS_PASSWORD)" ssh -p $(VPS_SSH_PORT) $(VPS_USER)@$(VPS_HOST) "cd ~/landinga && docker stack rm borrar || true && timeout /t 20 /nobreak && docker stack deploy -c $(STACK_FILE) --with-registry-auth borrar"

# Clean local Docker images
.PHONY: clean
clean:
	docker rmi $(IMAGE_NAME) 2>nul || exit 0