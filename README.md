Learn-Apache-Thrift
===================

This Python Module implements a simple load balancer using Apache Thrift.

All the files can be found in `lb/` directory

## Overview
It's a client server program. 2 instances of the servers must be running before client initiates load balancing. Each server has a single file on it. The server program differentiates servers based on ports. Once 2 instances of the server are running, the client can initiate load balancing by calling `load_balnce` service generated by Apache Thrift.

## Logical Diagram
client --------> Server A ------> Server B <br />
client <-------- Server A <------ Server B

## Services Implemented
* get_file
* prepend_file
* load_balance

## What does Load Balance do in this module?
It is a simple load balance. It takes last `n` lines from the file on server A, truncates the file on server A and sends these `n` lines to server B, prepends these `n` lines to the file on server B.

## Running
Copy the folder `lb` into your thrift installation directory

Creating Service stubs

`sudo thrift --gen py lb.thrift`

Running Server

`python lb_server.py <port> <file>`

Running Client

`python lb_client.py <src_port> <number_of_lines> <dest_port>`

## Testing
Create Big Files

`dd if=/dev/urandom of=a.txt bs=1048576 count=1000` # This creates 1GB File

`dd if=/dev/urandom of=b.txt bs=1048576 count=10` # This creates 10MB File

Start Server A with port number of your choice (say 9095 in this case) and the file of possission a.txt

`python lb_server.py 9095 a.txt` 

Start Server B with port number of your choice (say 9096 in this case) and the file of possission b.txt

`python lb_server.py 9096 b.txt` 

Start Client and speicify source port number, number of lines to transfer from a.txt to b.txt, and destination port number

`python lb_client.py 9095 10 9096`


## References:
* http://www.manning.com/abernethy/tPGtApacheThrift_MEAP_ch1.pdf
* [ImportError: No module named Thrift] http://thrift-tutorial.readthedocs.org/en/latest/usage-example.html
* http://stackoverflow.com/questions/11645876/how-to-efficiently-append-a-new-line-to-the-starting-of-a-large-file
* http://stackoverflow.com/questions/11020935/how-do-i-split-one-file-into-two-files-using-python
* http://stackoverflow.com/questions/11020935/how-do-i-split-one-file-into-two-files-using-python
* http://stackoverflow.com/questions/3895482/python-quickest-way-to-split-a-file-into-two-files-randomly
* http://stackoverflow.com/questions/11043372/how-to-use-pythons-tempfile-namedtemporaryfile
* http://stackoverflow.com/questions/5344287/create-read-from-tempfile
* http://stackoverflow.com/questions/8745387/in-python-make-a-tempfile-in-the-same-directory-as-another-file
* http://stackoverflow.com/questions/1659659/how-to-write-a-memory-efficient-python-program
