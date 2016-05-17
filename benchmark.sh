#!/bin/bash

if [ ! -f ab ]; then
    echo "Please install ab tool"
fi

echo "HOST: localhost:8080"

I=1000
C=10
F=2000
echo "Benchmarking iterations=$I concurrency=$C fib_num=$F"

time ab -n $I -c $C http://0.0.0.0:8080/fib/$F
