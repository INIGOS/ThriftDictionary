port = 9071

import sys, glob
sys.path.append('gen-py')
sys.path.insert(0, glob.glob('../../lib/py/build/lib.*'))
from extract import *
from extract.ttypes import *

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
import pickle , re, collections ,os , sys , inspect , traceback
cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
from Twokenize import twokenize
from Twokenize import emoticons
path = cmd_folder+"/models/"


class extractHandler(object):
    def __init__(self):
        self.acronyms=self.load_obj("acronymsDict")
        self.emoticons=self.load_obj("SmileyDict")
        self.answer={}
    def ping(self):
        print 'ping()'
    def load_obj(self,name):
        with open( path + name + '.pkl' , 'rb') as f:
            return pickle.load(f)
    def extract(self,text):
        emo_list=[]
        acr_list=[]

        for word in twokenize.tokenize(text):
            if word !=" ":
                word=word.strip()

                try:
                    score=self.emoticons[word]
                    emo=emoticons.analyze_tweetHeavy(word)
                    emo_list.append(emo)
                    self.answer['EMOTICONS']=emo_list
                except:

                    if "@" in word:
                        word="@user"
        text=text.lower()
        for word in twokenize.tokenize(text):
            if word!="":
                word=word.strip()
                
                try:
                    word=self.acronyms[word]
                    acr_list.append(word)
                    self.answer['EXPANDED ACRONYMS']=acr_list
                except:
                    if "@" in word:
                        word="@user"
        str1=str(self.answer)
        return str1

        #return self.answer
	#return "hey "



    def zip(self):
        print 'zip()'

handler = extractHandler()
processor = extratcionservice.Processor(handler)
transport = TSocket.TServerSocket(port=port)
tfactory = TTransport.TBufferedTransportFactory()
pfactory = TBinaryProtocol.TBinaryProtocolFactory()

server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)


print "Starting python server..."
server.serve()
print 'done.'
