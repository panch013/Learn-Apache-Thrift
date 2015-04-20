import sys,os,tempfile 
from shutil import copy,copy2,copyfileobj
from itertools import islice, chain 
sys.path.append("gen-py") 
from lb import LBSvc 
from thrift.transport import TSocket 
from thrift.transport import TTransport 
from thrift.protocol import TBinaryProtocol 
from thrift.server import TServer 

import inspect

def lineno():
    """Returns the current line number in our program."""
    return inspect.currentframe().f_back.f_lineno

class LBHandler: 
  def __init__(self, port, file_):
    self.port = port
    self.file_ = file_

  '''
  Function: get_file
  argumnets : number of lines to get
  return: last N lines and number of lines in the file
  '''
  def get_file(self, n):
    print("[Server]: Handling Shrink Request")
    try:
      if n == 0:
        return None
      with open(self.file_, 'rb') as source:
        with tempfile.NamedTemporaryFile() as out1:
          for i, line in enumerate(source):
           out1.write(line)
           if i == n-1:
             break
          out1.seek(0)
          # Return a file in a binary format. 
          # In future, divide it in chunks(system specific)
          lastNlines_bin = out1.read()
        with open('out_2', 'wb') as out2:
          out2.writelines(source)  
        os.rename('out_2', self.file_)
    except IOError:
      print("[Server]: File %s doesn't exist" % self.file_)
      return None
    
    print("[Server]: Done with splitting")
    return lastNlines_bin 

  '''
  Function: prepend_file_list
  argumnets : last N lines from the file on the first server 
  return: Nothing
  '''
  def prepend_file_list(self, lastNlines): 
    print("[Server]: Handling Prepend request")
    if len(lastNlines) == 0:
      print("[Server]: Nothing to prepend")
      return
    try:
      with open(self.file_, 'r') as infile, open("tmpfile", 'w+') as outfile:
        outfile.writelines(line for line in chain((lastNlines,), infile))
      copy("tmpfile", self.file_)
    except IOError:
      print ("[Server]: File '%s' Does not Exist" % self.file_)
      print ("[Server]: Opening a new File with the name '%s'" % self.file_)
      with open(self.file_, 'w') as infile:
        outfile.writelines(line for line in chain((lastNlines,), infile))
        
    print("[Server]: Done Prepending")

  '''
  Function: prepend_file
  argumnets : last N lines from the file on the first server 
  return: Nothing
  '''
  def prepend_file(self, lastNlines_bin): 
    print("[Server]: Handling Prepend request")
    try:
      with open(self.file_, 'rb') as infile, open("tmpfile", 'wb+') as outfile:
        # In future, Handle Chunks here
        #outfile.write(lastNlines_bin)
        outfile.writelines(line for line in lastNlines_bin)
        #outfile.write(infile.read())
        outfile.writelines(line for line in infile)
      os.rename("tmpfile", self.file_)
    except IOError:
      print ("[Server]: File '%s' Does not Exist" % self.file_)
      print ("[Server]: Opening a new File with the name '%s'" % self.file_)
      with open(self.file_, 'w') as infile:
        outfile.writelines(line for line in chain((lastNlines,), infile))
        
    print("[Server]: Done Prepending")

  '''
  Function: load_balance
  argumnets : number of lines to shrink the file on Server A and Server B port
              on which the the last 'n' lines from Server A will be prepended 
  return: Nothing
  '''
  def load_balance(self, n, b_port):
    lastNlines_bin = self.get_file(n)
    if lastNlines_bin == None:
      print("[Server]: Nothing to load balance") 
      return

    trans_ep = TSocket.TSocket("localhost", b_port) 
    trans_buf = TTransport.TBufferedTransport(trans_ep) 
    proto = TBinaryProtocol.TBinaryProtocol(trans_buf) 
    client = LBSvc.Client(proto) 
    trans_ep.open() 
    print ("[Server]: Established Connection with port: %s" % b_port)
    
    client.prepend_file(lastNlines_bin)   

    print("[Server]: Done Load Balancing")
    trans_ep.close() 

if len(sys.argv) < 3:
  print("[Server]: Usage # python lb_server.py <port> <file>")
  sys.exit(2)
handler = LBHandler(int(sys.argv[1]), sys.argv[2]) 
proc = LBSvc.Processor(handler) 

trans_ep = TSocket.TServerSocket(port=handler.port) 
trans_fac = TTransport.TBufferedTransportFactory() 
proto_fac = TBinaryProtocol.TBinaryProtocolFactory() 
server = TServer.TSimpleServer(proc, trans_ep, trans_fac, proto_fac) 
server.serve() 
