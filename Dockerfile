# Use an official Python runtime as a parent image
FROM --platform=linux/amd64 python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in pyproject.toml
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

# Make port available to the world outside this container
EXPOSE $PORT

# Run the application when the container launches
CMD uvicorn gesetze_im_netz.main:app --host 0.0.0.0 --port $PORT
