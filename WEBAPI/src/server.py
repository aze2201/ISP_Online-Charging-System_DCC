#!/usr/bin/python 
# coding=utf-8
from bottle import Bottle, run, template,request, response
import urllib2
import ast
from dbclient import clientConnection
from ConfigParser import SafeConfigParser
import sqlite3
parser = SafeConfigParser()


parser.read('../config/config.ini')
dbFile = parser.get('DBFILE', 'PATH')




exct=clientConnection()
exct.FirstConnect()


def dict_factory(cursor, row):
 d = {}
 for idx, col in enumerate(cursor.description):
  d[col[0]] = str(row[idx]).encode('utf8')
 return d
 

conn=sqlite3.connect(dbFile ,check_same_thread=False,isolation_level=None)
conn.row_factory = dict_factory


# return da exception sehv gedir.

app = Bottle()


@app.route('/Insert', method='POST')
def sqlInsert():
	result={}
	SQL="insert into "
	tableName=request.json["tableName"]
	columns=request.json["columns"]
	values=request.json["values"]
	SQL=SQL+str(tableName)+" "
	cols=""
	for column in columns:
		cols=cols+column+","
	cols=" ("+str(cols[:-1])+") "
	vals=""
	for val in values:
		vals=vals+"'"+val+"'"+","
	vals=" ("+vals[:-1]+") "
	SQL=SQL+cols+" values "+vals
	try:
		exct.SendRecv(SQL)
		result={'STATUS':'OK'}
	except Exception as e:
		result={'STATUS':str(e)}
	return result


@app.route('/Delete', method='POST')
def sqlDelete():
	result={}
	SQL="delete from "
	tableName=request.json["tableName"]
	condition=request.json["condition"]
	SQL=SQL+tableName+" WHERE "+condition
	try:
		exct.SendRecv(SQL)
		result={'STATUS':'OK'}
	except Exception as e:
		result={'STATUS':str(e)}
	return result

@app.route('/Update', method='POST')
def Update():
	result={}
	SQL="UPDATE "+str(request.json["tableName"])+" set "
	updateSettings=request.json["set"]
	condition=request.json["condition"]
	for k, v in updateSettings.iteritems():
		SQL=SQL+str(k)+"="+str(v)+","
	SQL=SQL[:-1]+" WHERE "+str(condition)
	try:
		exct.SendRecv(SQL)
		result={'STATUS':'OK'}
		#result=SQL
	except Exception as e:
		result={'STATUS':str(e)}
	return result
	
@app.route('/Select', method='POST')
def Select():
	result={}
	tableName=request.json["tableName"]
	SQL="select * from "+str(tableName)+" WHERE "
	try:
		condition=request.json["condition"]
		SQL=SQL+str(condition)
	except:
		condition=" 1=1"
		SQL=SQL+str(condition)
	try:
		result=str(conn.execute(SQL).fetchall())
	except Exception as e:
		result={'STATUS':str(e)}
	return result


run(app, host='0.0.0.0', port=7000,reloader=True,debug=True)
