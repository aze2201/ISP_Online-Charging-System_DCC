#!/usr/bin/python
# coding=utf-8
import socket
import pickle

from ConfigParser import SafeConfigParser
parser = SafeConfigParser()
parser.read('../config/config.ini')


host = parser.get('DBSERVER', 'IP')
port = int(parser.get('DBSERVER', 'PORT'))     

BUFFER_SIZE = 1024

class clientConnection:
	def __init__(self):
		self.tcpClientA = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.tcpClientA.connect((host, port))
	
	def wrap(self,message):
		result=message.split('ChargeDB > ')[1]
		return result
	
	def FirstConnect(self):
		firstMessageForConnect='\n'
		self.tcpClientA.send(firstMessageForConnect)
		return self.tcpClientA.recv(BUFFER_SIZE)
	
	def SendRecv(self,MESSAGE):
		result=''
		self.tcpClientA.send(MESSAGE)
		result=pickle.loads(self.tcpClientA.recv(BUFFER_SIZE))
		#result=self.wrap(result)
		return (result)


