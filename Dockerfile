# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements and script into the container
COPY requirements.txt requirements.txt
COPY anime-issue-creator.py anime-issue-creator.py

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Environment variable for GitHub token
ENV GITHUB_TOKEN=""

# Run the script
CMD ["python", "anime-issue-creator.py"]
