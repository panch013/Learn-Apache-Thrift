Learn-Apache-Thrift
===================

This Python Module implements a simple load balancer using Apache Thrift.
All the files can be found in `lb/` directory

## Overview:
It's a client server program. 2 instances of the servers must be running before client initiates load balancing. Each server has a single file on it. The server program differentiates servers based on ports. Once 2 instances of the server are running, the client can initiate load balancing by calling `load_balnce` service generated by Apache Thrift.

## Services Implemented:
* shrink_file
* prepend_file
* load_balance

## What does Load Balance do?
It takes last `n` lines from the file on server A, truncates the file on server A and sends these `n` lines to server B, prepends these `n` lines to the file on server B.

## References:
* http://www.manning.com/abernethy/tPGtApacheThrift_MEAP_ch1.pdf
* http://thrift-tutorial.readthedocs.org/en/latest/usage-example.html
