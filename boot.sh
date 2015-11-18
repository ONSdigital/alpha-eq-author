#!/bin/bash

platform='unknown'

OS="`uname`"
case $OS in
  'Linux')
    platform='Linux'
    ;;
  'Darwin')
    platform='Mac'
    ;;
  'WindowsNT'|*'CYGWIN'*)
    platform='Windows'
    ;;
  *) ;;
esac

echo "Running on $platform"

if (( "$platform" == "Windows" || "$platform" == "Mac" )); then
    echo "Starting docker-machine..."
    docker-machine start default
    eval "$(docker-machine env default)"
    echo "DOCKER_MACHINE_NAME=$DOCKER_MACHINE_NAME"
    echo "DOCKER_HOST=$DOCKER_HOST"
fi

if [ $? -eq 0 ]; then
    echo "Building docker containers..."
    docker-compose build
fi

if [ $? -eq 0 ]; then
    echo "Starting docker containers..."
    docker-compose up
fi
