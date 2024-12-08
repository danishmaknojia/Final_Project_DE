export PORT = 8080

# Define the image name and Docker Hub username
IMAGE_NAME_LOCAL = ids706_cbb
IMAGE_NAME_ECR = ids706_cbb
DOCKER_ID_USER = nakiyah24

# Default port if not set
PORT ?= 8080

# Target to run tests before proceeding with other tasks
test:
	@echo "Running tests..."
	python3 -m pytest -vv tests/test_*.py
	@echo "Tests completed successfully!"

lint:
	ruff check *.py mylib/*.py

# Build the Docker image
build:
	docker build -t $(IMAGE_NAME_LOCAL):latest .


# Run the Docker container
# Forward $(PORT) on the host to port 8080 in the container
run:
	docker run -p $(PORT):8080 -e PORT=$(PORT) $(IMAGE_NAME_LOCAL)

# Stop and remove all containers associated with the image, then delete the image
clean:
	-docker ps -a -q --filter ancestor=$(IMAGE_NAME_LOCAL) | xargs -r docker stop
	-docker ps -a -q --filter ancestor=$(IMAGE_NAME_LOCAL) | xargs -r docker rm
	-docker images -q $(IMAGE_NAME_LOCAL) | xargs -r docker rmi -f

# Show all Docker images
image_show:
	docker images

# Show all running containers
container_show:
	docker ps

# Push the image to Docker Hub or Amazon ECR
push:
	@echo "Logging in to AWS ECR..."
	aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 381492212823.dkr.ecr.us-east-1.amazonaws.com
	@echo "Tagging image..."
	docker tag $(IMAGE_NAME_LOCAL):latest 381492212823.dkr.ecr.us-east-1.amazonaws.com/$(IMAGE_NAME_ECR):latest
	@echo "Pushing image to ECR..."
	docker push 381492212823.dkr.ecr.us-east-1.amazonaws.com/$(IMAGE_NAME_ECR):latest


# Describe repos
# aws ecr describe-repositories --repository-names project --region us-east-1

# Push to Docker Hub (Optional)
push_docker_hub:
	docker login
	docker tag $(IMAGE_NAME_LOCAL) $(DOCKER_ID_USER)/$(IMAGE_NAME_LOCAL):latest
	docker push $(DOCKER_ID_USER)/$(IMAGE_NAME_LOCAL):latest

# Login to Docker Hub
login:
	docker login -u ${DOCKER_ID_USER}
