import sys, glob
sys.path.append('gen-py')
sys.path.insert(0, glob.glob('../../lib/py/build/lib.*'))


from extract import *
from extract.ttypes import *


from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol


try:

	transport=TSocket.TSocket('localhost',9092)
	
	transport=TTransport.TBufferedTransport(transport)

	protocol=TBinaryProtocol.TBinaryProtocol(transport)

	client=extratcionservice.Client(protocol)
	transport.open()
	
	client.ping()
	print "ping()"

	text="hey hello :p , today is tuesday :) rofl and LOL the weather is :p too hot @ chennai :( :p lol , ok ciao "
	output=client.extract(text)
#replace SmileyOperation by AcronymsOperation to get all the acronmys present in the given text
	print output

	transport.close()

except Thrift.TException, tx:
	print '%s' % (tx.message)


