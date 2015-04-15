import sys 
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

  def shrink_file(self, file_, n):
    print("[Server]: Handling Shrink request")
    try:
      fileObject = open(file_, "rw+")
      print("[Server]: File Opened: ", file_)
    except IOError:
      print ("[Server]: File '{file_}' Does not Exist")
   
    lastNlines = fileObject.readlines()[-n:]
    fileObject.seek(0,2) 
    size = fileObject.tell()
    print("[Server]: Size of the file: ", size)
    fileObject.truncate(size-n)
    fileObject.close() 
    print("[Server]: Done Shrinking")
    return lastNlines 

  def prepend_file(self, file_, lastNlines): 
    print("[Server]: Handling Prepend request")
    try:
      fileObject = open(file_, "rw+")
      print("[Server]: File Opened: ", file_)
      old_data = fileObject.read() 
      fileObject.close()
    except IOError:
      print ("[Server]: File '{file_}' Does not Exist")
      print ("[Server]: Opening a new File '{file_}'")
      fileObject = open(file_, "w")

    fileObject = open(file_, "rw+")
    for line in lastNlines:
      fileObject.write(line)
    fileObject.write(old_data)
    fileObject.close()

  #TODO Remove a_port?
  def load_balance(self, a_port, n, b_port):
    lastNlines = self.shrink_file(self.file_, n)

    print("[Server]: lastNlines")
    print lastNlines
    trans_ep = TSocket.TSocket("localhost", b_port) 
    trans_buf = TTransport.TBufferedTransport(trans_ep) 
    proto = TBinaryProtocol.TBinaryProtocol(trans_buf) 
    client = LBSvc.Client(proto) 
    trans_ep.open() 
    print ("[Server]: Established Connection with port: ", b_port)
    
    #client.prepend_file(client.file_, lastNlines)   
 
    print("[Server]: Done Load Balancing")
    trans_ep.close() 

handler = LBHandler(int(sys.argv[1]), sys.argv[2]) 
proc = LBSvc.Processor(handler) 

trans_ep = TSocket.TServerSocket(port=handler.port) 
trans_fac = TTransport.TBufferedTransportFactory() 
proto_fac = TBinaryProtocol.TBinaryProtocolFactory() 
server = TServer.TSimpleServer(proc, trans_ep, trans_fac, proto_fac) 
server.serve() 
