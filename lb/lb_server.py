import sys 
sys.path.append("gen-py") 
from lb import LBSvc 
from thrift.transport import TSocket 
from thrift.transport import TTransport 
from thrift.protocol import TBinaryProtocol 
from thrift.server import TServer 

class LBHandler: 
  def shrink_file(self, file_, n):
    print("[Server]: Handling Shrink request")
    try:
      fileObject = open(file_, "rw+")
      print("[Server]: File Opened")
    except IOError:
      print ("[Server]: File '{file_}' Does not Exist")
   
    lastNlines = fileObject.readlines()[-n:]
    fileObject.seek(0,2) 
    size = fileObject.tell()
    fileObject.truncate(size-n)
    fileObject.close() 
    return lastNlines 

  def prepend_file(self, file_, lastNlines): 
    print("[Server]: Handling Prepend request")
    try:
      fileObject = open(file_, "rw+")
      print("[Server]: File Opened")
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

  def load_balance(self, a_port, a_file, n, b_port, b_file):
    lastNlines = self.shrink_file(a_file, n)
    self.prepend_file(b_file, lastNlines)

handler = LBHandler() 
proc = LBSvc.Processor(handler) 

trans_ep = TSocket.TServerSocket(port=9095) 
trans_fac = TTransport.TBufferedTransportFactory() 
proto_fac = TBinaryProtocol.TBinaryProtocolFactory() 
server = TServer.TSimpleServer(proc, trans_ep, trans_fac, proto_fac) 
server.serve() 
