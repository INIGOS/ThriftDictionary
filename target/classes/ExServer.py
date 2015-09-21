port = 9071

import sys, glob
sys.path.append('gen-py')
sys.path.insert(0, glob.glob('../../lib/py/build/lib.*'))
from thriftinterface import *
from thriftinterface.ttypes import *
#from ExAcro import *
#from ExAcro.ttypes import *
#from ExEmo import *
#from ExEmo.ttypes import *
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
    def ExEmo(self,text):
        emo_list=[]
        store_emo={}
    
        for word in twokenize.tokenize(text):
            if word !=" ":
                word=word.strip()
    
                try:
                    score=self.emoticons[word]
                    emo=emoticons.analyze_tweetHeavy(word)
                    #emo_list.append(word)#
                    #emo_list.append(emo)
                    #d=dict(itertools.izip_longest(*[iter(emo_list)] * 2, fillvalue=""))
                    store_emo[word]=emo
                except:
    
                    if "@" in word:
                        word="@user"
        self.answer=store_emo
        str1=str(self.answer)
        return str1
    
    def ExAcro(self,text):
        acr_list=[]
        text=text.lower()
        store_acronyms={}
        for word in twokenize.tokenize(text):
            if word!="":
                word=word.strip()
                
                try:
                    word_after=self.acronyms[word]
                    #acr_list.append(word)
                    store_acronyms[word]=word_after
                    #self.answer['EXPANDED ACRONYMS']=acr_list
                except:
                    if "@" in word:
                        word="@user"
        self.answer=store_acronyms
        str2=str(self.answer)
        return str2
    
        #return self.answer
    #return "hey "
    
    
    
    def zip(self):
        print 'zip()'

handler = extractHandler()
processor = extractionservice.Processor(handler)
transport = TSocket.TServerSocket(port=port)
tfactory = TTransport.TBufferedTransportFactory()
pfactory = TBinaryProtocol.TBinaryProtocolFactory()

server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)


print "Starting python server..."
server.serve()
print 'done.'
