#!/bin/bash

WRK_BIN=wrk2
WRK_SCRIPT=./testnp.lua
URL=http://localhost:5000

# runs a benchmark for 3 seconds, using 5 threads, keeping 20 HTTP connections open
# and a constant throughput of 20 requests per second (total, across all connections combined).
#$WRK_BIN -d60s -c16 -t8 -R160 --u_latency -s $WRK_SCRIPT $URL
$WRK_BIN -d30s -c20 -t10 -R50 --latency -s $WRK_SCRIPT $URL
