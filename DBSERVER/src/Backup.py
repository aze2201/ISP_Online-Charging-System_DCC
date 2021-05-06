
import time
import threading
import datetime

class Backup(threading.Thread)
	def __init__(conn,period):
		threading.Thread.__init__(self)
		self.conn=conn
		self.BackupPath=
		self.TableList4Backup=
		self.DBNAME='disk'
		self.period=period
		
	def run(self):
		while True:
			print "--------------------------------------"+str(datetime.datetime.now())
			for TableName in TableList4Backup:
				try:
					self.conn.execute("DROP TABLE "+TableName)
					print "Table dropped " + TableName
				except Exception as e:
					print "Some problem while DROP TABLE : "+e+" : "+TableName
				sqlsting="CREATE TABLE "+self.DBNAME+"."+TableName+" as SELECT * FROM TableName"
				try:
					self.conn.execute(sqlsting)
					print "Table backed up fully: "+TableName
				except Exception as e:
					print "Some problem while take backup table : "+e+" : "+TableName+
			print "--------------------------------------"+str(datetime.datetime.now())
			time.sleep(self.period)

	
		

