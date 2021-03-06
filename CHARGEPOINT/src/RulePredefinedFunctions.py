from dbclient import clientConnection
exct=clientConnection()
exct.FirstConnect()

import datetime

def getSubcriberStatus(SubsID):
	result=''
	SQL="SELECT STATUS FROM SUBCRIBER_STATUS WHERE SUBSCRIBER_ID="+str(SubsID)
	try:
		result=str(exct.SendRecv(SQL)[0][0]).encode('utf-8')
	except:
		result='3000'
	return int(result)

def getOfferCost(OfferID):
	result=''
	SQL="SELECT Value FROM PRICE T INNER JOIN Price2Offer O on O.PriceID=T.PriceID WHERE OfferID="+str(OfferID)
	try:
		result=exct.SendRecv(SQL)[0][0]
	except:
		result='3000'
	return result

def genSQLinsert(JSONstring,CC_TIME):
	result=''
	values=''
	fields=''
	SQL="INSERT INTO SESSION "
	for key in JSONstring.keys():
		fields=fields+','+key
		values=values+"'"+str(JSONstring[key]).replace("'",'')+"',"
	values=" values ("+str(values[:-1])+",'"+str(CC_TIME)+"')"
	fields="("+fields[1:]+",StartTime)"
	SQL=SQL+fields+values
	try:
		exct.SendRecv(SQL)
		result={'STATUS':'OK'}
	except:
		result={'STATUS':'NOOK'}
	return result

def genSQLupdate(JSONstring,CC_TIME):
	result=''
	SQL="update session set EndTme="+str(CC_TIME)+","
	setVal=''
	condition=" WHERE AccountID='"
	for key in JSONstring.keys():
		setVal=setVal+str(key)+"='"+str(JSONstring[key]).replace("'",'')+"',"
	condition=condition+str(JSONstring['AccountID'])+"'"
	SQL=SQL+setVal[:-1]+condition
	try:
		exct.SendRecv(SQL)
		result={'STATUS':'OK'}
	except:
		result={'STATUS':'NOOK'}
	return result

def UpdateSessionTable(JSONstring,CC_TIME):
	result=''
	if JSONstring['CC_TYPE'].upper()=='INITIAL':
		result=genSQLinsert(JSONstring,CC_TIME)
	elif JSONstring['CC_TYPE'].upper() in ('UPDATE','TERMINATE'):
		result=genSQLupdate(JSONstring,CC_TIME)
	return result

def chargeAccount(CC_TYPE,accoundID,ServiceType,balance):
	result=''
	if CC_TYPE=='TERMINATE':
		SQL="update balance set "
		if ServiceType == 0:
			Balance= "MAIN_BALANCE = MAIN_BALANCE - "+str(balance)
			SQL=SQL+Balance
			SQL=SQL + " WHERE ACCOUNTID = "+str(accoundID)
			try:
				exct.SendRecv(SQL)
				result={'STATUS':'OK'}
			except:
				result={'STATUS':'NOOK'}
		elif ServiceType == 1:
			Balance= "DATA_BALANCE = DATA_BALANCE - "+str(balance)
			SQL=SQL+Balance
			SQL=SQL + " WHERE ACCOUNTID = "+str(accoundID)
			try:
				exct.SendRecv(SQL)
				result={'STATUS':'OK'}
			except:
				result={'STATUS':'NOOK'}
		return result

def ReserveChargeAmountDATA(AccountID,Reserve,CC_TIME,GrantedTime=None,sign=None):
	result={}
	SQL=''
	if sign=='P':
		SQL="UPDATE BALANCE SET DATA_BALANCE=ABS(DATA_BALANCE-"+str(Reserve)+") WHERE ACCOUNTID="+str(AccountID)
	else:
		SQL="UPDATE BALANCE SET DATA_BALANCE=DATA_BALANCE-"+str(Reserve)+" WHERE ACCOUNTID="+str(AccountID)
	try:
		exct.SendRecv(SQL)
		if Reserve > 0:
			result={'AccountID':AccountID,'AMOUNT':DataReserve,'Result-Code':'2001','CC_TIME':CC_TIME}
	except:
		result={'AccountID':AccountID,'AMOUNT':DataReserve,'Result-Code':'3999','CC_TIME':CC_TIME}
	return result

def ReserveAmountVOICE(AccountID,Reserve,CC_TIME,GrantedTime=None,sign=None):
	# This both functions need to include Minutes also. How much need to wait for CCR
	result={}
	SQL=''
	if sign=='P':
		SQL="UPDATE BALANCE SET DATA_BALANCE=ABS(MAIN_BALANCE-"+str(Reserve)+") WHERE ACCOUNTID="+str(AccountID)
	else:
		SQL="UPDATE BALANCE SET DATA_BALANCE=DATA_BALANCE-"+str(Reserve)+" WHERE ACCOUNTID="+str(AccountID)
	try:
		exct.SendRecv(SQL)
		if Reserve > 0:
			result={'AccountID':AccountID,'AMOUNT':Reserve,'Result-Code':'2001','CC_TIME':CC_TIME,'GrantedTime':GrantedTime}
	except:
		result={'AccountID':AccountID,'AMOUNT':Reserve,'Result-Code':'3999','CC_TIME':CC_TIME,'GrantedTime':GrantedTime}
	return result


def getBalance(AccountID):
	result={}
	SQL="SELECT MAIN_BALANCE,DATA_BALANCE FROM BALANCE WHERE ACCOUNTID="+str(AccountID)
	try:
		balance=exct.SendRecv(SQL)[0]
		result={'MAIN_BALANCE':balance[0],'DATA_BALANCE':balance[1]}
	except:
		result='3000'
	return (result)

def getAccount(SubsID):
	result=''
	SQL="SELECT ACCOUNTID FROM SUBSCRIBER2ACCOUNT WHERE SUBSCRIBER_ID="+str(SubsID)
	try:
		result=str(exct.SendRecv(SQL)[0][0]).encode('utf-8')
	except:
		result='3000' 
	return result

def getOffer(AccID):
	result=''
	SQL="SELECT OfferID FROM OFFER2ACCOUNT WHERE ACCOUNTID="+str(AccID)
	try:
		result=str(exct.SendRecv(SQL)[0][0]).encode('utf-8')
	except:
		result='3001'
	return result

def getProductID(OfferID,ServiceType=None):
	# ServiceType need to provided by AVP
	result={}
	SQL="SELECT T.ProductID,Z.ProductType,z.ReserveAmount,ProductFee,LimitAmount,ServiceType FROM Product2Offer T INNER JOIN Product Z on Z.ProductID=T.ProductID WHERE T.OfferID="+str(OfferID)
	try:
		result=exct.SendRecv(SQL)[0]
		if len(result)==6:
			result={'ProductID':result[0],'ProductType':str(result[1]).encode('utf-8'),'ReserveAmount':result[2],'ProductFee':result[3],'LimitAmount':result[4],'ServiceType':result[5]}
		else:
			result={'ProductID':'MULTIPLE DATA FOUND','ProductType':'MULTIPLE DATA FOUND'}
	except:
		result=['3002']
	return result

def getPolicy(PrdcID):
	result=''
	SQL="SELECT PolicyID FROM Policy2Product WHERE ProductID="+str(PrdcID)
	try:
		result=str(exct.SendRecv(SQL)[0][0]).encode('utf-8')
	except:
		res='3003'
	return result

def getTimeSchema(PolicyID):
	# this is will return LIST
	result=[]
	SQL="SELECT t.TSchemaID FROM TimeSchema2Policy t inner join TimeSchema z on z.TSchemaID=t.TSchemaID WHERE t.PolicyID="+str(PolicyID)
	SQL=SQL+" order by z.Priority"
	try:
		tmpResult=exct.SendRecv(SQL)
		for ID in tmpResult:
			result.append(str(ID[0]).encode('utf-8'))
	except:
		result='3004'
	return result

def getTimeSchemaOrder(TSIDList):
	result=[]
	SQL="SELECT TschemaType FROM TimeSchema WHERE TSchemaID in ("
	for TSID in TSIDList:
		SQL=SQL+"'"+str(TSID)+"',"
	SQL=SQL[:-1]+")"
	result=exct.SendRecv(SQL)
	return result

def RateByRate(TSList):
	# it will get ordered TimeSchemaID and will get TypeOfRate y/m/w/d/h
	# it will call TypeOfRate function based on TimeSchemID
	options = {
		1 : Yearly,
		2 : MonthOfYear,
		3 : DayOfMonth,
		4 : DayOfWeek,
		5 : HourOfDay,
                6 : MinOfHour
		}
	rate=1
	print str(TSList)
	for rt in getTimeSchemaOrder(TSList):
		rate =  rate * options[rt[0]](TSList)
	return rate

def PricingPerUnit(ProductFee,ReserveAmount,LimitAmount):
	result={}
	Price=ProductFee * ReserveAmount / LimitAmount
	result={'PRICE':Price,'AMOUNT':ReserveAmount}
	return result

#
# THIS FUNCTIONS WILL GET POSITION OF PROPERTY BY CURRENT /Y/M/W/D/H and will call Rating which is joined to current Position
#

def Yearly (TSID):
	# 1  2017-2018
	result=''
	currPosition=datetime.datetime.today().year
	SQL="SELECT r.RateID, t.Property,r.RateValue FROM TimeSchema t inner join Rate2TimeSchema rt on t.TSchemaID=rt.TSchemaID inner join Rate r on r.RateID=rt.RateID WHERE t.TSchemaID in ("
	for id in TSID:
		SQL=SQL+"'"+str(id)+"',"
	SQL=SQL[:-1]+") and t.TschemaType=1 and r.Property="+str(currPosition)
	try:
		result=exct.SendRecv(SQL)[0][2]
	except Exception as e:
		result=e
	return result

def MonthOfYear(TSID):
	# 12 000000000011
	result=''
	currPosition=datetime.datetime.today().month
	SQL="SELECT r.RateID, t.Property,r.RateValue FROM TimeSchema t inner join Rate2TimeSchema rt on t.TSchemaID=rt.TSchemaID inner join Rate r on r.RateID=rt.RateID WHERE t.TSchemaID in ("
	for id in TSID:
		SQL=SQL+"'"+str(id)+"',"
	SQL=SQL[:-1]+") and t.TschemaType=2 and r.RateJOIN=substr(Property,"+str(currPosition)+",1)"
	try:
		result=exct.SendRecv(SQL)[0][2]
	except Exception as e:
		result=e
	return result

def DayOfWeek(TSID):
	# 7 00000011
	currPosition=datetime.datetime.today().weekday()+1
	result=''
	SQL="SELECT r.RateID, t.Property,r.RateValue FROM TimeSchema t inner join Rate2TimeSchema rt on t.TSchemaID=rt.TSchemaID inner join Rate r on r.RateID=rt.RateID WHERE t.TSchemaID in ("
	for id in TSID:
		SQL=SQL+"'"+str(id)+"',"
	SQL=SQL[:-1]+") and t.TschemaType=4 and r.RateJOIN=substr(Property,"+str(currPosition)+",1)"
	try:
		result=exct.SendRecv(SQL)
		result=result[0][2]
	except Exception as e:
		result=e
	return result

def DayOfMonth  (TSID):
	# 31 0000000000000000000000000000001
	currPosition=datetime.datetime.now().day
	SQL="SELECT r.RateID, t.Property,r.RateValue FROM TimeSchema t inner join Rate2TimeSchema rt on t.TSchemaID=rt.TSchemaID inner join Rate r on r.RateID=rt.RateID WHERE t.TSchemaID in ("
	for id in TSID:
		SQL=SQL+"'"+str(id)+"',"
	SQL=SQL[:-1]+") and t.TschemaType=3 and r.RateJOIN=substr(Property,"+str(currPosition)+",1)"
	try:
		result=exct.SendRecv(SQL)[0][2]
	except Exception as e:
		result=e
	return result

	
def HourOfDay (TSID):
	# 24 000000000000000000001111
	currPosition=datetime.datetime.now().hour
	result=''
	SQL="SELECT r.RateID, t.Property,r.RateValue FROM TimeSchema t inner join Rate2TimeSchema rt on t.TSchemaID=rt.TSchemaID inner join Rate r on r.RateID=rt.RateID WHERE t.TSchemaID in ("
	for id in TSID:
		SQL=SQL+"'"+str(id)+"',"
	SQL=SQL[:-1]+") and t.TschemaType=5 and r.RateJOIN=substr(Property,"+str(currPosition)+",1)"
	try:
		result=exct.SendRecv(SQL)[0][2]
	except Exception as e:
		result=e
	return result



def MinOfHour  (TSID):
	# 60 111111111111111111111111111111111111111111111111111111111111
	currPosition=datetime.datetime.now().minute
	SQL="SELECT r.RateID, t.Property,r.RateValue FROM TimeSchema t inner join Rate2TimeSchema rt on t.TSchemaID=rt.TSchemaID inner join Rate r on r.RateID=rt.RateID WHERE t.TSchemaID in ("
	for id in TSID:
		SQL=SQL+"'"+str(id)+"',"
	SQL=SQL[:-1]+") and t.TschemaType=6 and r.RateJOIN=substr(Property,"+str(currPosition)+",1)"
	try:
		result=exct.SendRecv(SQL)[0][2]
	except Exception as e:
		result=e
	return result
