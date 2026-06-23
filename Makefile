# Makefile for Tecticom project (Windows Version)

# Variables de entorno en Windows se leen con %VAR% o $(variable)
IMAGE_NAME = ghcr.io/19ramirez/docker-flask:1.0.0
STACK_FILE = stack.yml
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
	@echo   deploy     Deploy stack to VPS (scp stack.yml and Makefile)
	@echo   clean      Remove local Docker images

# Build Docker image
.PHONY: build
build:
	docker build -t $(IMAGE_NAME) .

# Push image to GHCR (requires GHCR_PAT env var)
# Nota: En Windows, 'echo %VAR%' funciona diferente. Usamos un pipe limpio.
.PHONY: push
push:
	@echo | set /p="$(GHCR_PAT)" | docker login ghcr.io -u $(GITHUB_ACTOR) --password-stdin
	docker push $(IMAGE_NAME)

# Deploy to VPS (uses sshpass for password authentication)
# En Windows (CMD), la continuación de línea se hace con ^ y las cadenas de SSH usan comillas simples/dobles invertidas de forma estricta.
.PHONY: deploy
deploy:
	@echo Copying $(STACK_FILE) and Makefile to VPS...
	sshpass -p "$(VPS_PASSWORD)" ssh -p $(VPS_SSH_PORT) $(VPS_USER)@$(VPS_HOST) "cd ~/despliegue && docker stack rm tecticom || true && timeout /t 30 /nobreak && docker stack deploy -c $(STACK_FILE) --with-registry-auth tecticom"

# Clean local Docker images
.PHONY: clean
clean:
	docker rmi $(IMAGE_NAME) 2>nul || exit 0