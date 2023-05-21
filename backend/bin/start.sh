#!/bin/bash

set -x

# $@ accepts optional arguments like `--reload`
uvicorn src.app:app --host 0.0.0.0 --port ${BACKEND_PORT} $@
