# Define the image name and Docker Hub username
IMAGE_NAME = nd191_assignment12
DOCKER_ID_USER = nakiyah24

# Default port if not set
PORT ?= 5005

# Build the Docker image
build:
	docker build -t $(IMAGE_NAME):latest .


# Run the Docker container
# Forward $(PORT) on the host to port 5000 in the container
run:
	docker run -p $(PORT):5000 $(IMAGE_NAME)

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

# Push the image to Docker Hub
push:
	docker login
	docker tag $(IMAGE_NAME) $(DOCKER_ID_USER)/$(IMAGE_NAME)
	docker push $(DOCKER_ID_USER)/$(IMAGE_NAME):latest

# Login to Docker Hub
login:
	docker login -u ${DOCKER_ID_USER}
