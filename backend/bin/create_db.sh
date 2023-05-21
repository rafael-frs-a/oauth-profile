#!/bin/bash

set -x

# Will create configured database if it does not exist
python -m src.cli.create_db
