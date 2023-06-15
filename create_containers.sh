#!/bin/bash

docker build -t lambda task

for i in {0..4}; do
    docker container create --name lambda_"$i" -p 900"$i":8080 lambda
done
