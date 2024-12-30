# Include environment variables
ENV_FILE = $(PWD)/.env
include $(ENV_FILE)

# Check for required environment variables
.PHONY: check-env
check-env:
	@if [ -z "$(DOCKER_IMAGE)" ]; then echo "DOCKER_IMAGE is not set"; exit 1; fi
	@if [ -z "$(DOCKER_CONTAINER)" ]; then echo "DOCKER_CONTAINER is not set"; exit 1; fi
	@if [ -z "$(LOCAL_PORT)" ]; then echo "LOCAL_PORT is not set"; exit 1; fi
	@if [ -z "$(PROJECT_ID)" ]; then echo "PROJECT_ID is not set"; exit 1; fi
	@if [ -z "$(APP_NAME)" ]; then echo "APP_NAME is not set"; exit 1; fi
	@if [ -z "$(REGION)" ]; then echo "REGION is not set"; exit 1; fi
	@if [ -z "$(REACT_APP_OPENAI_API_KEY)" ]; then echo "OPENAI_API_KEY is not set"; exit 1; fi
	@if [ -z "$(REACT_APP_ANTHROPIC_API_KEY)" ]; then echo "ANTHROPIC_API_KEY is not set"; exit 1; fi
	@if [ -z "$(SERVICE_ACCOUNT)" ]; then echo "SERVICE_ACCOUNT is not set"; exit 1; fi

# Variables
NODE_MODULES_DIR = node_modules
DIST_DIR = dist

# Build the Docker image for Google Cloud Run
.PHONY: build-cloud
build-cloud: check-env
	docker build -t gcr.io/$(PROJECT_ID)/$(APP_NAME) .

# Deploy to Google Cloud Run
.PHONY: deploy-cloud
deploy-cloud: build-cloud
	gcloud run deploy $(APP_NAME) --image gcr.io/$(PROJECT_ID)/$(APP_NAME) --platform managed --region $(REGION) --allow-unauthenticated

# Retrieve the service URL
.PHONY: get-url
get-url:
	@echo "Service URL:"
	@gcloud run services describe $(APP_NAME) --platform managed --region $(REGION) --format "value(status.url)"

# Clean up local Docker images
.PHONY: clean-cloud
clean-cloud:
	docker rmi gcr.io/$(PROJECT_ID)/$(APP_NAME)
