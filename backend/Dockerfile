# Base image
FROM python:3.10-slim as base

# Initiate workdir
RUN mkdir -p /app/backend
WORKDIR /app/backend

# Update package list
# Install `curl` for docker-compose health-check
# Install `psycopg2` dependencies
# Clean up package list cache
RUN apt-get update && \
    apt-get install -y curl libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

# Copy dependency files first to avoid reinstalling them unless these specific files change
COPY requirements*.txt ./

# Multi-stage environments

# `dev` environment
FROM base as dev
# Ensure `requirements.txt` and `requirements-dev.txt` common packages have same version
# `pip install` should fail if there is any mismatch
RUN pip install --no-cache-dir -r requirements.txt -r requirements-dev.txt
COPY ./ ./

# `test` environment
FROM base as test
# Ensure `requirements.txt` and `requirements-dev.txt` common packages have same version
# `pip install` should fail if there is any mismatch
RUN pip install --no-cache-dir -r requirements.txt -r requirements-dev.txt
COPY ./ ./
# Disable potential python breakpoints left
ENV PYTHONBREAKPOINT=0

# `prod` environment
FROM base as prod
RUN pip install --no-cache-dir -r requirements.txt
COPY ./ ./
# Disable potential python breakpoints left
ENV PYTHONBREAKPOINT=0
