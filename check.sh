#!/bin/bash

TESTSUITE=testsuite
LIST="misc.py fib-service.py"

export PYTHONPATH=service

echo "HOST: localhost:8080"

for i in $LIST
do
	echo "Test: $i"
	python "$TESTSUITE/$i"
done
