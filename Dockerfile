# Use a base image with Python and Flask installed
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the application code into the container
COPY . /app

# Install the required dependencies including Flask and Andrew Ng's AI suite library
RUN pip install --no-cache-dir -r requirements.txt

# Set the entry point to run the Flask app
CMD ["python", "app.py"]
