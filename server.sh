#!/bin/bash

docker build -t game-server -f Dockerfile.server .

docker run -t -p 1234:1234 game-server
