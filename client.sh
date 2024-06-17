#!/bin/bash

docker build -t game-client -f Dockerfile.client .

xhost +local:docker

sudo docker run -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -t game-client
