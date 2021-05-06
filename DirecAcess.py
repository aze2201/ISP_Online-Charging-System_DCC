from socket import *
import thread
import sqlite3
from ConfigParser import SafeConfigParser
parser = SafeConfigParser()
parser.read('../config/config.ini')


BUFF = 1024
HOST = parser.get('DBSERVER', 'IP')
PORT = parser.get('DBSERVER', 'PORT')               # must be input parameter @TODO
DATABASE="file:memdb1?mode=memory&cache=shared"

print "Server started with "+str(HOST)+" | "+src(PORT)


conn=sqlite3.connect(DATABASE ,check_same_thread=False,isolation_level=None)

def get_by_address(address):
    return [x for x in globals().values() if id(x)==address]


class SQLiteDirectAccess:
	def __init__(self):
		self.connection=conn
		print self.connection
		
	def exct(self,data):
		result=''
		try:
			result=conn.execute(data).fetchall()
		except Exception as e:
			result=e
		return result
		
def dict_factory(cursor, row):
 d = {}
 for idx, col in enumerate(cursor.description):
  d[col[0]] = str(row[idx]).encode('utf8')
 return d

conn.row_factory = dict_factory

def response(key):
	result=''
	try:
		#result=conn.execute(key).fetchall()
		result=MemoryClass.exct(key)
	except Exception as e:
		result=e
	return result
	#return 'Server response: ' + key

def handler(clientsock,addr):
    while 1:
        data = clientsock.recv(BUFF)
        if not data: break
        print repr(addr) + ' recv:' + repr(data)
        clientsock.send(str("ChargeDB > ")+str(response(data)))
        #print repr(addr) + ' sent:' + repr(response(data))
        if "close" == data.rstrip(): break # type 'close' on client console to close connection from the server side

    clientsock.close()
    print addr, "- closed connection" #log on console

if __name__=='__main__':
    ADDR = (HOST, PORT)
    MemoryClass=SQLiteDirectAccess()
    serversock = socket(AF_INET, SOCK_STREAM)
    serversock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serversock.bind(ADDR)
    serversock.listen(5)
    while 1:
        print 'waiting for connection... listening on port', PORT
        clientsock, addr = serversock.accept()
        print '...connected from:', addr
        thread.start_new_thread(handler, (clientsock, addr))