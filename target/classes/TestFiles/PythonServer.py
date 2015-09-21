import sys, glob
sys.path.append('gen-py')
sys.path.insert(0, glob.glob('../../lib/py/build/lib.*'))

from tutorial import Calculator
from tutorial.ttypes import *

from shared.ttypes import SharedStruct

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

class CalculatorHandler:
  def __init__(self):
    self.log = {}

  def ping(self):
    print 'ping()'

  def add(self, n1, n2):
    print 'add(%d,%d)' % (n1, n2)
    return n1+n2

  

  def getStruct(self, key):
    print 'getStruct(%d)' % (key)
    return self.log[key]

  def zip(self):
    print 'zip()'

handler = CalculatorHandler()
processor = Calculator.Processor(handler)
transport = TSocket.TServerSocket(port=9099)
tfactory = TTransport.TBufferedTransportFactory()
pfactory = TBinaryProtocol.TBinaryProtocolFactory()

server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

# You could do one of these for a multithreaded server
#server = TServer.TThreadedServer(processor, transport, tfactory, pfactory)
#server = TServer.TThreadPoolServer(processor, transport, tfactory, pfactory)

print 'Starting the server...'
server.serve()
print 'done.'
