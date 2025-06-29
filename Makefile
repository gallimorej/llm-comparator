# Include environment variables
ENV_FILE = $(PWD)/.env
include $(ENV_FILE)

# Check for required environment variables
.PHONY: check-env
check-env:
	@if [ -z "$(DOCKER_IMAGE)" ]; then echo "DOCKER_IMAGE is not set"; exit 1; fi
	@if [ -z "$(DOCKER_CONTAINER)" ]; then echo "DOCKER_CONTAINER is not set"; exit 1; fi
	@if [ -z "$(PORT)" ]; then echo "PORT is not set"; exit 1; fi
	@if [ -z "$(PROJECT_ID)" ]; then echo "PROJECT_ID is not set"; exit 1; fi
	@if [ -z "$(APP_NAME)" ]; then echo "APP_NAME is not set"; exit 1; fi
	@if [ -z "$(REGION)" ]; then echo "REGION is not set"; exit 1; fi
	@if [ -z "$(OPENAI_API_KEY)" ]; then echo "OPENAI_API_KEY is not set"; exit 1; fi
	@if [ -z "$(ANTHROPIC_API_KEY)" ]; then echo "ANTHROPIC_API_KEY is not set"; exit 1; fi
	@if [ -z "$(SERVICE_ACCOUNT)" ]; then echo "SERVICE_ACCOUNT is not set"; exit 1; fi
	@if [ -z "$(GOOGLE_PROJECT_ID)" ]; then echo "GOOGLE_PROJECT_ID is not set"; exit 1; fi
	@if [ -z "$(GOOGLE_REGION)" ]; then echo "GOOGLE_REGION is not set"; exit 1; fi
	@if [ -z "$(GOOGLE_APPLICATION_CREDENTIALS)" ]; then echo "GOOGLE_APPLICATION_CREDENTIALS is not set"; exit 1; fi

# Variables
# NODE_MODULES_DIR = node_modules
# DIST_DIR = dist
DOCKERFILE = Dockerfile

# Run the application in Docker
.PHONY: build-docker
build-docker: check-env
	docker build --platform linux/amd64 -t $(DOCKER_IMAGE) -f $(DOCKERFILE) .

.PHONY: run-docker
run-docker: build-docker
	docker run --env-file $(ENV_FILE) -p $(PORT):$(PORT) --name $(DOCKER_CONTAINER) $(DOCKER_IMAGE)

# Stop and remove the Docker container
.PHONY: clean-docker
clean-docker:
	docker stop $(DOCKER_CONTAINER) || true
	docker rm $(DOCKER_CONTAINER) || true

# Enable necessary APIs
.PHONY: enable-apis
enable-apis:
	gcloud services enable run.googleapis.com
	gcloud services enable artifactregistry.googleapis.com
	gcloud services enable containerregistry.googleapis.com

# Build the Docker image for Google Cloud Run
.PHONY: build-cloud
build-cloud: check-env
	docker build --platform linux/amd64 -t gcr.io/$(PROJECT_ID)/$(APP_NAME) .
	docker push gcr.io/$(PROJECT_ID)/$(APP_NAME)

# Deploy to Google Cloud Run
.PHONY: deploy-cloud
deploy-cloud: build-cloud
	gcloud run deploy $(APP_NAME) --image gcr.io/$(PROJECT_ID)/$(APP_NAME) --platform managed --region $(REGION) --allow-unauthenticated --port $(PORT) --set-env-vars="PROJECT_ID=$(PROJECT_ID),SERVICE_ACCOUNT=$(SERVICE_ACCOUNT),CONFIG_BUCKET_NAME=$(CONFIG_BUCKET_NAME),ANTHROPIC_API_KEY=$(ANTHROPIC_API_KEY),OPENAI_API_KEY=$(OPENAI_API_KEY),GOOGLE_PROJECT_ID=$(GOOGLE_PROJECT_ID),GOOGLE_REGION=$(GOOGLE_REGION),GOOGLE_APPLICATION_CREDENTIALS=$(GOOGLE_APPLICATION_CREDENTIALS)"

# Clean up local Docker images
.PHONY: clean-cloud
clean-cloud:
	docker rmi gcr.io/$(PROJECT_ID)/$(APP_NAME)

# Get the service URL
APP_URL := $(shell gcloud run services describe $(APP_NAME) --platform managed --region $(REGION) --format "value(status.url)")

# Retrieve the service URL
.PHONY: get-url
get-url:
	@echo "Service URL:"
	@echo "$(APP_URL)"

# Update the config in Google Cloud Storage
.PHONY: update-config
update-config: check-env
	@if [ ! -f "static/config.json" ]; then \
		echo "Error: static/config.json not found"; \
		exit 1; \
	fi
	@echo "Uploading config.json to gs://$(CONFIG_BUCKET_NAME)/config.json..."
	@gsutil cp static/config.json gs://$(CONFIG_BUCKET_NAME)/config.json
	@echo "Config uploaded successfully"
	@echo "Refreshing config in the application..."
	@curl -s -X POST $(APP_URL)/api/refresh_config | grep -q '"success":true' && echo "Config refreshed successfully" || (echo "Failed to refresh config" && exit 1)
