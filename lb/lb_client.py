
import sys
sys.path.append("gen-py")
from lb import LBSvc 
from thrift.transport import TSocket 
from thrift.transport import TTransport 
from thrift.protocol import TBinaryProtocol 

trans_ep = TSocket.TSocket("localhost", 9095) 
trans_buf = TTransport.TBufferedTransport(trans_ep) 
proto = TBinaryProtocol.TBinaryProtocol(trans_buf) 
client = LBSvc.Client(proto) 
trans_ep.open() 
#msg = client.shrink_file("a.txt", 2) 
#print("[Client]: received: %s" % msg) 
#client.prepend_file("b.txt", msg)
#print("[Clinet]: File prepended")
client.load_balance(9095, "a.txt", 2, 9096, "b.txt")
print("[Client]: Done Load Balancing")
