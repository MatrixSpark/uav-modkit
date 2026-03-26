#!/usr/bin/env bash
set -e

docker build -f docker/Dockerfile -t uav-modkit:jazzy .
echo "Docker image built: uav-modkit:jazzy"
