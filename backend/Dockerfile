# Use a slim Python base image
FROM python:3.11-slim

# Prevent Python from writing pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies (git is required for cloning repos during scans)
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install --no-cache-dir poetry

# Configure Poetry to install directly into the system environment (Docker provides isolation)
RUN poetry config virtualenvs.create false

# Copy the poetry dependency files first (for Docker cache optimization)
COPY pyproject.toml poetry.lock* ./

# Install dependencies (ignoring the root package and dev dependencies)
RUN poetry install --no-root --only main

# Create a non-root user for security
RUN addgroup --system appgroup && adduser --system --group appuser

# Copy the rest of the backend application code
COPY . .

# Transfer ownership to the non-root user
RUN chown -R appuser:appgroup /app

# Drop root privileges
USER appuser

# Expose the standard FastAPI port
EXPOSE 8000

# Start the uvicorn server. 
# Since main.py is inside the "app" folder, we call "app.main:app"
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]