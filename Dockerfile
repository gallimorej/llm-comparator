# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt requirements.txt

# Install the dependencies
RUN pip install -r requirements.txt

# Copy the service account key file first
COPY gen-lang-client-0765726668-c4d842188ce5.json /app/

# Copy the rest of the application code into the container
COPY . .

# Set the environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=3000

# Expose the port the app runs on
EXPOSE 3000

# Run the Flask app
CMD ["flask", "run"]