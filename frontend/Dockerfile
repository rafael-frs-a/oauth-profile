# Base image
FROM node:16-alpine3.17 as base

# Initiate workdir
RUN mkdir -p /app/frontend
WORKDIR /app/frontend

# Install `bash` to run sh files
RUN apk update && apk add bash

# Copy dependency files first to avoid reinstalling them unless these specific files change
COPY package*.json ./

# Multi-stage environments

# `dev` environment
FROM base as dev
RUN npm install
COPY ./ ./

# `test` environment
FROM base as test
RUN npm install
COPY ./ ./
RUN npm run build

# `prod` environment
FROM base as prod
# Many dev-packages are needed for the building step
RUN npm install
COPY ./ ./
RUN npm run build
# Removing dev-packages after building
RUN npm prune --production
