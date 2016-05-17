Fibonacci series web service
===================

This is a simple web service which intended
to calculate Fibonacci series.

Requirements
---

* Python 2.7+
* web.py module
* [Optional, need for benchmarking] ab tool

Start service
---

Use ./service/fib.py --help to see usage of the service.

Example
  ./service/fib.py --verbose --cache-size 2000
This will start the service (at localhost, port 8080)
and pre-initialize internal cache with first
2000 Fibonacci numbers. This also will enable verbose
output to the console.

Testing
---

To run funtional testing:
  ./check.sh

To benchmark your server:
  ./benchmark.sh
