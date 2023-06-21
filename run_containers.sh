#!/bin/bash

docker build -t worker worker

for i in {0..4}; do
    if [ ! "$(docker ps -aq -f name=worker_"$i")" ]; then
        docker run -d --name worker_"$i" -p 900"$i":5000 worker
    else
        docker start worker_"$i"
    fi
done