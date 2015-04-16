
import sys
sys.path.append("gen-py")
from lb import LBSvc 
from thrift.transport import TSocket 
from thrift.transport import TTransport 
from thrift.protocol import TBinaryProtocol 

if len(sys.argv) < 4:
  print("[Client]: Usage # python lb_client.py <src_port> <num_of_lines> <dest_port>")
  sys.exit(2)
trans_ep = TSocket.TSocket("localhost", int(sys.argv[1])) 
trans_buf = TTransport.TBufferedTransport(trans_ep) 
proto = TBinaryProtocol.TBinaryProtocol(trans_buf) 
client = LBSvc.Client(proto) 
trans_ep.open() 
client.load_balance(int(sys.argv[2]), int(sys.argv[3]))
print("[Client]: Done Load Balancing")
trans_ep.close() 

