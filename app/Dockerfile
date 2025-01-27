# Use the official Python base image
FROM python:3.12.7

# Update the package lists
RUN apt-get update

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to working directory
COPY ./requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/app

# Copy all the code
# requirements is copied seperately to create a layer so that pip install exec is cached
COPY ./app /app

# Expose port 8000 for the FastAPI app
EXPOSE 8000

# Default command (can be overridden by Docker Compose) 
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]