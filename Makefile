export PORT = 8080

# Define the image name and Docker Hub username
IMAGE_NAME = de_project
DOCKER_ID_USER = nakiyah24

# Default port if not set
PORT ?= 8080

# Build the Docker image
build:
	docker build -t $(IMAGE_NAME):latest .


# Run the Docker container
# Forward $(PORT) on the host to port 5000 in the container
run:
	docker run -p $(PORT):8080 -e PORT=$(PORT) $(IMAGE_NAME)

# Stop and remove all containers associated with the image, then delete the image
clean:
	-docker ps -a -q --filter ancestor=$(IMAGE_NAME) | xargs -r docker stop
	-docker ps -a -q --filter ancestor=$(IMAGE_NAME) | xargs -r docker rm
	-docker images -q $(IMAGE_NAME) | xargs -r docker rmi -f

# Show all Docker images
image_show:
	docker images

# Show all running containers
container_show:
	docker ps

# Push the image to Docker Hub or Amazon ECR
push:
	docker login
	aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 381492212823.dkr.ecr.us-east-1.amazonaws.com
	docker tag $(IMAGE_NAME):latest 381492212823.dkr.ecr.us-east-1.amazonaws.com/de_project:latest
	docker push 381492212823.dkr.ecr.us-east-1.amazonaws.com/de_project:latest

# Describe repos
# aws ecr describe-repositories --repository-names project --region us-east-1

# Push to Docker Hub (Optional)
push_docker_hub:
	docker login
	docker tag $(IMAGE_NAME) $(DOCKER_ID_USER)/$(IMAGE_NAME):latest
	docker push $(DOCKER_ID_USER)/$(IMAGE_NAME):latest

# Login to Docker Hub
login:
	docker login -u ${DOCKER_ID_USER}
