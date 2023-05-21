#!/bin/bash

set -x

if [ "$1" = "dev" ]; then
  npm run dev -- -p ${FRONTEND_PORT}
else
  npm run start -- -p ${FRONTEND_PORT}
fi
