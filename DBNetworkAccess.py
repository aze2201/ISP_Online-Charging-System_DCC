#!/usr/bin/python

from ConfigParser import SafeConfigParser
import json
import urllib2

"""
THIS IS BASIC DB CLIENT

data={"SQL":"select * from disk.abc"}
a=DbClient('config.ini')
a.execute("select * from abc")
"""


class DbClient:
	def __init__(self,FileName):
		self.FileName=FileName
		self.parser = SafeConfigParser()
		self.parser.read(self.FileName)
		self.data=None
		self.URL=self.parser.get('dbinfo', 'url')
		
	def SQL(self,data):
		self.data={"SQL":data}
	
	def execute(self,JsonSQL):
		data=self.SQL(JsonSQL)
		result={}
		try:
			req = urllib2.Request(self.URL)
			req.add_header('Content-Type', 'application/json')
			result=urllib2.urlopen(req, json.dumps(self.data)).read()
			#print result
		except Exception as msg:
			result=msg
		return result
