#!/bin/bash

sed -i 's/127\.0\.0\.1/34.32.65.191/g' ./client/views/server_list.py

docker build -t game-client -f Dockerfile.client .

xhost +local:docker

sudo docker run -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -t game-client
