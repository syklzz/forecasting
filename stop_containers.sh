#!/bin/bash

for i in {0..4}; do
    docker stop worker_"$i"
done