import sys,os 
sys.path.append("gen-py") 
from lb import LBSvc 
from thrift.transport import TSocket 
from thrift.transport import TTransport 
from thrift.protocol import TBinaryProtocol 
from thrift.server import TServer 

class LBHandler: 
  def __init__(self, port, file_):
    self.port = port
    self.file_ = file_

  def get_lines(self, n):
    print("[Server]: Getting last N lines")
   
    try:
      info = []
      lastNlines = []   
      num_lines = 0
      fileObject = open(self.file_, "rw+")
      num_lines = sum(1 for line in fileObject) 
      # If the number of lines to be transferred are
      # more then the number of lines in the file, 
      # transfer all the lines
      if n > num_lines:
        n = num_lines
      # File doesn't contain any lines
      if num_lines == 0:
        print("[Server]: The File has 0 lines. Nothing to Shrink in the File: %s" % self.file_)
        info.append(lastNlines) 
        info.append(num_lines)
        return info 
      print("[Server]: File Opened: ", self.file_)
    except IOError:
      print ("[Server]: File '%s' Does not Exist" % self.file_)
      info.append(lastNlines) 
      info.append(num_lines)
      return info 
 
    fileObject = open(self.file_, "rw+")
    for i, line in enumerate(fileObject):
      if i >= (num_lines - n):
        lastNlines.append(line)
   
    info.append(lastNlines) 
    info.append(num_lines)
    print("[Server]: Got Last N Lines")
    return info 

  def shrink_file(self, n, num_lines):
    print("[Server]: Handling Shrink request")
   
    if n > num_lines:
      n = num_lines
      # File doesn't contain any lines
    if num_lines == 0:
      print("[Server]: The File has 0 lines. Nothing to Shrink in the File: %s" % self.file_)
      return
    
    with open(self.file_, "r+") as fileObject:
      for x in xrange(num_lines - n):
        fileObject.readline()
      fileObject.truncate()
    fileObject.close() 

    print("[Server]: Done Shrinking")

  def prepend_file(self, lastNlines): 
    print("[Server]: Handling Prepend request")
    if len(lastNlines) == 0:
      print("[Server]: Nothing to prepend")
      return
    try:
      old_data = None
      fileObject = open(self.file_, "rw+")
      old_data = fileObject.read() 
      fileObject.close()
    except IOError:
      print ("[Server]: File '%s' Does not Exist" % self.file_)
      print ("[Server]: Opening a new File with the name '%s'" % self.file_)
      fileObject = open(self.file_, "w+")

    fileObject = open(self.file_, "rw+")
    for line in lastNlines:
      fileObject.write(line)
    if old_data:
      fileObject.write(old_data)
    fileObject.close()
    print("[Server]: Done Prepending")

  def load_balance(self, n, b_port):
    info = self.get_lines(n)
    lastNlines = info[0]
    num_lines = int(info[1]) 

    if len(lastNlines) == 0:
      print("[Server]: Nothing to Load Balance") 
      return

    trans_ep = TSocket.TSocket("localhost", b_port) 
    trans_buf = TTransport.TBufferedTransport(trans_ep) 
    proto = TBinaryProtocol.TBinaryProtocol(trans_buf) 
    client = LBSvc.Client(proto) 
    trans_ep.open() 
    print ("[Server]: Established Connection with port: ", b_port)
    
    client.prepend_file(lastNlines)   

    # Shrink the File only if the prepend is successful
    self.shrink_file(n, num_lines)

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
