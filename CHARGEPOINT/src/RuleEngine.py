
from RulePredefinedFunctions import *


#ChargeReserve({'SubsID':555056210,'ServiceType':1,'USEDTIME':0,'CC_TYPE':'INITIAL'},2018020323470000)

def ChargeReserve(InputJson,CC_TIME):
	SubsID=InputJson['SubsID']
	try:
		ServiceType=InputJson['ServiceType']
		ChargeInfo['ServiceType']=InputJson['ServiceType']
	except:
		ServiceType = 0
	ChargeInfo = {}
	result = {}
	ChargeInfo['USEDTIME'] = InputJson['USEDTIME']
	ChargeInfo['StatusSubcriber'] = getSubcriberStatus(SubsID) 
	ChargeInfo['CC_TYPE'] = InputJson['CC_TYPE']
	if ChargeInfo['StatusSubcriber']==1:
		ChargeInfo['AccountID'] = getAccount(SubsID)
		ChargeInfo['BALANCE'] = getBalance(ChargeInfo['AccountID']) 
		ChargeInfo['OfferID'] = getOffer(ChargeInfo['AccountID'])
		ChargeInfo['ProductProperty'] = getProductID(ChargeInfo['OfferID'],ServiceType)        
		ChargeInfo['OfferCost'] = getOfferCost(ChargeInfo['OfferID'])
		if ChargeInfo['ProductProperty']['ServiceType'] == 0 :             
			ChargeInfo['PolicyID'] = getPolicy(ChargeInfo['ProductProperty']['ProductID'])
			ChargeInfo['TimeSchema'] = getTimeSchema(ChargeInfo['PolicyID'])
			ChargeInfo['Rate'] = RateByRate(ChargeInfo['TimeSchema'])
			ChargeInfo['ChargeBalance'] = ChargeInfo['USEDTIME'] * ChargeInfo['ProductProperty']['ProductFee'] / float(ChargeInfo['ProductProperty']['LimitAmount'])
			ChargeInfo['FinalCharge'] = ChargeInfo['Rate']* ChargeInfo['ChargeBalance']
			ChargeInfo['maxUseTime'] = ChargeInfo['BALANCE']['MAIN_BALANCE'] * ChargeInfo['Rate'] * ChargeInfo['ProductProperty']['LimitAmount'] / ChargeInfo['ProductProperty']['ProductFee']
			ChargeInfo['maxUseAmount'] = ChargeInfo['BALANCE']['MAIN_BALANCE'] * ChargeInfo['Rate']
			if ChargeInfo['maxUseAmount'] > ChargeInfo['FinalCharge']:  # may be need to check expirtion time
				ChargeInfo['maxUseAmount'] = ChargeInfo['maxUseAmount'] - ChargeInfo['FinalCharge']
				ChargeInfo['maxUseTime'] = ChargeInfo['maxUseTime'] - ChargeInfo['USEDTIME']
				if ChargeInfo['maxUseTime'] > ChargeInfo['ProductProperty']['ReserveAmount']:
					UpdateSessionTable(ChargeInfo,CC_TIME)
					result={'Reserved':ChargeInfo['ProductProperty']['ReserveAmount'],'ACCOUNT':ChargeInfo['AccountID'],'CC_TIME':CC_TIME}
					chargeAccount(ChargeInfo['CC_TYPE'],ChargeInfo['AccountID'],ChargeInfo['ProductProperty']['ServiceType'],ChargeInfo['FinalCharge'])
				else:
					UpdateSessionTable(ChargeInfo,CC_TIME)
					result={'Reserved':ChargeInfo['maxUseTime'],'ACCOUNT':ChargeInfo['AccountID'],'CC_TIME':CC_TIME}
					chargeAccount(ChargeInfo['CC_TYPE'],ChargeInfo['AccountID'],ChargeInfo['ProductProperty']['ServiceType'],ChargeInfo['FinalCharge'])
			elif ChargeInfo['maxUseAmount'] <= ChargeInfo['FinalCharge']:
				if ChargeInfo['maxUseAmount'] > 0:
					UpdateSessionTable(ChargeInfo,CC_TIME)
					result={'Reserved':ChargeInfo['maxUseTime'],'ACCOUNT':ChargeInfo['AccountID'],'CC_TIME':CC_TIME}
					chargeAccount(ChargeInfo['CC_TYPE'],ChargeInfo['AccountID'],ChargeInfo['ProductProperty']['ServiceType'],ChargeInfo['FinalCharge'])
			else:
				result={'status':4999}   # bunu function return ucun saxla DIAMETER mesage'a elave ele
	return result
	
	#if Message is terminater then update balance 