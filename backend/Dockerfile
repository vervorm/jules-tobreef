# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
# --no-cache-dir ensures that pip doesn't store the downloaded packages, reducing image size.
# --trusted-host pypi.python.org can be useful if there are SSL issues with PyPI.
RUN pip install --no-cache-dir --trusted-host pypi.python.org -r requirements.txt

# Copy the rest of the backend application code into the container at /app
COPY . .

# Copy the frontend files into a location that the Flask app expects.
# The Flask app in __init__.py is configured with:
# frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'frontend'))
# If WORKDIR is /app (which is 'backend' content), then __file__ is /app/app/__init__.py
# os.path.dirname(__file__) is /app/app
# '..' is /app
# '..' is /
# 'frontend' becomes /frontend
# So we need to copy the local 'frontend' directory to '/frontend' in the image.
COPY ../frontend /frontend

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variables (optional, but can be useful)
ENV FLASK_APP run.py
ENV FLASK_RUN_HOST 0.0.0.0
ENV FLASK_RUN_PORT 5000
# ENV FLASK_DEBUG True # Set to True for development, but be cautious in prod

# Run run.py when the container launches
# The backend/run.py needs to be adjusted to use host='0.0.0.0'
CMD ["python", "run.py"]
