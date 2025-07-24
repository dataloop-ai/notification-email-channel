#!/bin/bash

docker build --platform=linux/amd64 --no-cache -t gcr.io/viewo-g/piper/agent/runner/cpu/node14-py10:latest -f Dockerfile .
docker push gcr.io/viewo-g/piper/agent/runner/cpu/node14-py10:latest