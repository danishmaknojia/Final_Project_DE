# Use the official Python image from Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install necessary Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8080 for App Runner
EXPOSE 8080

# Define environment variable for Flask
ENV FLASK_APP=app.py

# Run the Flask app when the container launches
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080", "--debug"]
