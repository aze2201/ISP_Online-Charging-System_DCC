from socket import *
import thread
import sqlite3

BUFF = 1024
HOST = '0.0.0.0'
PORT = 4321
DATABASE="file:memdb1?mode=memory&cache=shared"

print "Server started with "+str(HOST)+" | "+str(PORT)

conn=sqlite3.connect(DATABASE ,check_same_thread=False,isolation_level=None)

class SQLiteDirectAccess:
	def __init__(self):
		self.connection=conn
		print self.connection
		
	def exct(self,data):
		result=[]
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

#conn.row_factory = dict_factory

def response(key):
	result=[]
	try:
		result=MemoryClass.exct(key)
	except Exception as e:
		result=e
	return result

def handler(clientsock,addr):
    while 1:
        data = clientsock.recv(BUFF)
        if not data: break
        print repr(addr) + ' recv:' + repr(data)
        reply=response(data)
        reply=str(reply)
        clientsock.send(reply)
        if "close" == data.rstrip():
			clientsock.close()
			print addr, "- closed connection"
			break 								
			

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
