# Use the official Python image from Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install necessary system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libev-dev \
    libffi-dev \
    python3-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container
COPY . /app

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip wheel
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8080 for App Runner
EXPOSE 8080

# Define environment variable for Flask
ENV FLASK_APP=app.py

# Run the Flask app when the container launches
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080", "--debug"]
