# Base image
FROM python:3.10-slim as base

# Initiate workdir
RUN mkdir -p /app/e2e-tests
WORKDIR /app/e2e-tests

# Update package list
# Clean up package list cache
RUN apt-get update && \
    rm -rf /var/lib/apt/lists/*

# Copy dependency files first to avoid reinstalling them unless these specific files change
COPY requirements*.txt ./

# Multi-stage environments

# `prod` environment
FROM base as prod
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers
RUN playwright install --with-deps chromium

COPY ./ ./
# Disable potential python breakpoints left
ENV PYTHONBREAKPOINT=0
