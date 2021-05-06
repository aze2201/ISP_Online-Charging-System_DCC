#!/usr/bin/python  
#############################################################################  
# Example of diameter server listening client requests on port 3868   
# This script is using pyprotosim software  
# Read the terms of BSD license at pyprotosim website:  
# http://sourceforge.net/projects/pyprotosim/    
############################################################################  
import sys  
sys.path.append("../")  
# Remove them if everything is in the same dir  
import socket  
import select  
import logging  
from libDiameter import *  

import datetime
from RuleEngine import *

###########################################################################################  
# 
# users_db is dictionary with key identity, can be replaced connection to ldap db or sql db  
# 
###########################################################################################  
users_db = {'123456789012345':{'maxbytes':'10000000', 'sessionid':'value_1', 'usedbytes':'0','cctime':'0'},  
     '123456789012348':{'maxbytes':'20000000', 'sessionid':'value_2','usedbytes':'0','cctime':'0' },  
     '123456789012347':{'maxbytes':'30000000', 'sessionid':'value_3', 'usedbytes':'0','cctime':'0'}}

# Functions to check if user is valid in users_db database and fetch profile settings  
# Also upon receiving Credit-Control Initial request, update new session id for this user if exists  
def check_valid_user(identity):  
 id = identity  
 if id in users_db:  
  return True  
 else:  
  return False  
def update_sessionid(identity,sessionid):  
  id = identity  
  sessionid = sessionid  
  if id in users_db:  
   sessionid_updated = users_db[id]['sessionid']=sessionid  
   return sessionid_updated  
  else:  
   return False  
def check_profile(identity):  
 id=identity  
 if id in users_db:  
  maxbytes = users_db[id]['maxbytes']  
  cctime = users_db[id]['cctime']  
  return maxbytes,cctime  
 else:  
  return None
  
#check_profile=ChargeReserve({'SubsID':555056210,'CC_TYPE':'TERMINATE'},20170101)
"{'Result-Code': '2001', 'CC_TIME': 20170101, 'AMOUNT': 1024, 'AccountID': '555056210'}"

############END OF USER FUNCTIONS##############################  
# Starting tcp server on python listening requests on port 3868  
###############################################################  
SKIP=0  
def handle_OCS(conn):  
  global sock_list  
  # conn is the TCP socket connected to the client  
  dbg="Connection:",conn.getpeername(),'to',conn.getsockname()  
  logging.info(dbg)  
  #get input ,wait if no data  
  data=conn.recv(BUFFER_SIZE)  
  #suspect more data (try to get it all without stopping if no data)  
  if (len(data)==BUFFER_SIZE):  
    while 1:  
      try:  
        data+=self.request.recv(BUFFER_SIZE, socket.MSG_DONTWAIT)  
      except:  
        #error means no more data  
        break  
  if (data != ""):   
    #processing input  
    dbg="Incomming message",data.encode("hex")  
    logging.info(dbg)  
    ret=process_request(data.encode("hex"))   
    if ret==ERROR:  
      dbg="Error responding",ret  
      logging.error(dbg)  
    else:  
      if ret==SKIP:  
        dbg="Skipping response",ret  
        logging.info(dbg)          
      else:  
        dbg="Sending response",ret  
        logging.info(dbg)  
        conn.send(ret.decode("hex"))    
  else:  
    #no data found exit loop (posible closed socket)      
    # remove it from sock_list  
    sock_list.remove(conn)  
    conn.close()  
# Create CEA response to CER request  
# Just answering with 2001 OK      
def create_CEA(H):  
  global DEST_REALM  
  CER_avps=splitMsgAVPs(H.msg)  
  DEST_REALM=findAVP("Origin-Realm",CER_avps)    
  # Let's build Capabilites-Exchange Answer  
  CEA_avps=[]  
  CEA_avps.append(encodeAVP("Origin-Host", ORIGIN_HOST))  
  CEA_avps.append(encodeAVP("Origin-Realm", ORIGIN_REALM))  
  CEA_avps.append(encodeAVP("Product-Name", "OCS-SIM"))  
  CEA_avps.append(encodeAVP('Auth-Application-Id', 4))  
  CEA_avps.append(encodeAVP("Supported-Vendor-Id", 10415))  
  CEA_avps.append(encodeAVP("Result-Code", 2001))  #DIAMETER_SUCCESS 2001  
  # Create message header (empty)  
  CEA=HDRItem()  
  # Set command code  
  CEA.cmd=H.cmd  
  # Set Application-id  
  CEA.appId=H.appId  
  # Set Hop-by-Hop and End-to-End from request  
  CEA.HopByHop=H.HopByHop  
  CEA.EndToEnd=H.EndToEnd  
  # Add AVPs to header and calculate remaining fields  
  ret=createRes(CEA,CEA_avps)  
  # ret now contains CEA Response as hex string  
  return ret  
# Create Watchdog response in reply to Watchdog request . We reply with 2001 OK  
def create_DWA(H):  
  # Let's build Diameter-WatchdogAnswer   
  DWA_avps=[]  
  DWA_avps.append(encodeAVP("Origin-Host", ORIGIN_HOST))  
  DWA_avps.append(encodeAVP("Origin-Realm", ORIGIN_REALM))  
  DWA_avps.append(encodeAVP("Result-Code", 2001)) #DIAMETER_SUCCESS 2001  
  # Create message header (empty)  
  DWA=HDRItem()  
  # Set command code  
  DWA.cmd=H.cmd  
  # Set Application-id  
  DWA.appId=H.appId  
  # Set Hop-by-Hop and End-to-End from request  
  DWA.HopByHop=H.HopByHop  
  DWA.EndToEnd=H.EndToEnd  
  # Add AVPs to header and calculate remaining fields  
  ret=createRes(DWA,DWA_avps)  
  # ret now contains DWA Response as hex string  
  return ret  
# Create Disconnect_Peer response in reply to Disconnect_Peer request. We just reply with 2001 OK for testing purposes  
def create_DPA(H):  
  # Let's build Diameter-Disconnect Peer Answer  
  DPA_avps=[]  
  DPA_avps.append(encodeAVP("Origin-Host", ORIGIN_HOST))  
  DPA_avps.append(encodeAVP("Origin-Realm", ORIGIN_REALM))  
  DPA_avps.append(encodeAVP("Result-Code", 2001)) #DIAMETER_SUCCESS 2001  
  # Create message header (empty)  
  DPA=HDRItem()  
  # Set command code  
  DPA.cmd=H.cmd  
  # Set Application-id  
  DPA.appId=H.appId  
  # Set Hop-by-Hop and End-to-End from request  
  DPA.HopByHop=H.HopByHop  
  DPA.EndToEnd=H.EndToEnd  
  # Add AVPs to header and calculate remaining fields  
  ret=createRes(DPA,DPA_avps)  
  # ret now contains DPA Response as hex string  
  return ret  
# Create Unable To Comply response in reply to request which is not understood. We reply with 5012 result-code AVP  
def create_UTC(H,msg):  
  # Let's build Unable to comply packet  
  DWA_avps=[]  
  DWA_avps.append(encodeAVP("Origin-Host", ORIGIN_HOST))  
  DWA_avps.append(encodeAVP("Origin-Realm", ORIGIN_REALM))  
  DWA_avps.append(encodeAVP("Result-Code", 5012)) #UNABLE TO COMPLY 5012  
  DWA_avps.append(encodeAVP("Error-Message", msg))  
  # Create message header (empty)  
  DWA=HDRItem()  
  # Set command code  
  DWA.cmd=H.cmd  
  # Set Application-id  
  DWA.appId=H.appId  
  # Set Hop-by-Hop and End-to-End from request  
  DWA.HopByHop=H.HopByHop  
  DWA.EndToEnd=H.EndToEnd  
  # Add AVPs to header and calculate remaining fields  
  ret=createRes(DWA,DWA_avps)  
  # ret now contains DWA Response as hex string  
  return ret  
# And here we create CCA-I responses in reply to CCR -I requests:   
def create_CCA(H):
   # Added by Fariz for default values. Sometimes Request is not include this parameter 
   CCA_REQUEST_TYPE='1'
   valid_user=False
   CCA_SESSION='12345'
   CCA_IMSI='400040000000000'
   CCA_REQUEST_NUMBER=0
   # /Added by Fariz
   CCR_avps=splitMsgAVPs(H.msg)  
   try:  
    CCA_SESSION=findAVP("Session-Id",CCR_avps)  
    CCA_SSID=findAVP("Subscription-Id",CCR_avps)   
    CCA_IMSI=findAVP("Subscription-Id-Data",CCA_SSID)  
    CCA_REQUEST_TYPE=findAVP("CC-Request-Type",CCR_avps)    
    CCA_REQUEST_NUMBER=findAVP("CC-Request-Number",CCR_avps)  
    CCA_Unit=findAVP("Used-Service-Unit",CCR_avps)  
   except:  
    pass  
   if CCA_REQUEST_TYPE in [1]:  
   # Checking if user is valid in users_db:
    valid_user=check_valid_user(CCA_IMSI)         
   if valid_user is True:  
    # If user is valid in users_db, check profile settings and extract CC-Time and CC-Total-Octets  
    #max_bytes,cctime=check_profile(CCA_IMSI)
    CheckProfile=ChargeReserve({'SubsID':CCA_IMSI,'CC_TYPE':CCA_REQUEST_TYPE},20170101)
	max_bytes=CheckProfile['AMOUNT']
	cctime=CheckProfile['CC_TIME']
    # Update session id received from CCR request in users_db for this user  
    updated_sessionid=update_sessionid(CCA_IMSI,CCA_SESSION)  
    print str(datetime.datetime.now())+" Updated sessionid in DB is now: ",updated_sessionid  
    print str(datetime.datetime.now())+" User ",CCA_IMSI," has limit of: ",max_bytes,"bytes"  
    # Answer with CCA response:  
    CCA_avps=[ ]  
    CCA_avps.append(encodeAVP('Result-Code', '2001'))  
    CCA_avps.append(encodeAVP('Session-Id', CCA_SESSION))  
    CCA_avps.append(encodeAVP('Origin-Host', ORIGIN_HOST))  
    CCA_avps.append(encodeAVP('Origin-Realm', ORIGIN_REALM))  
    CCA_avps.append(encodeAVP('CC-Request-Type', CCA_REQUEST_TYPE))  
    CCA_avps.append(encodeAVP('CC-Request-Number', CCA_REQUEST_NUMBER+1))  
    CCA_avps.append(encodeAVP('Auth-Application-Id', 4))  
    CCA_avps.append(encodeAVP('Supported-Vendor-Id', 10415))  
    # Check for None values:  
    if str(max_bytes) != 'None' or str(cctime) != 'None':  
     CCA_avps.append(encodeAVP('Granted-Service-Unit',[  
    encodeAVP("CC-Total-Octets",int(max_bytes)),encodeAVP("CC-Time",int(cctime))  
    ]))  
     # Create message header (empty)  
    CCA=HDRItem()  
     # Set command code  
    CCA.cmd=H.cmd  
     # Set Application-id  
    CCA.appId=H.appId  
     # Set Hop-by-Hop and End-to-End from request  
    CCA.HopByHop=H.HopByHop  
    CCA.EndToEnd=H.EndToEnd  
     # Add AVPs to header and calculate remaining fields  
    ret=createRes(CCA,CCA_avps)  
     # ret now contains CCA Response as hex string        
    return ret  
   elif valid_user is False:  
    # If user is not found in DB, return 5003 - not authorized  
    print str(datetime.datetime.now())+" No such user ",CCA_IMSI," is found in DB:"  
    CCA_avps=[ ]  
    CCA_avps.append(encodeAVP('Result-Code', '5003'))  
    CCA_avps.append(encodeAVP('Session-Id', CCA_SESSION))  
    CCA_avps.append(encodeAVP('Origin-Host', ORIGIN_HOST))  
    CCA_avps.append(encodeAVP('Origin-Realm', ORIGIN_REALM))  
    CCA_avps.append(encodeAVP('CC-Request-Type', CCA_REQUEST_TYPE))  
    CCA_avps.append(encodeAVP('CC-Request-Number', CCA_REQUEST_NUMBER+1))  
    CCA_avps.append(encodeAVP('Auth-Application-Id', 4))  
    CCA_avps.append(encodeAVP('Supported-Vendor-Id', 10415))  
     # Create message header (empty)  
    CCA=HDRItem()  
     # Set command code  
    CCA.cmd=H.cmd  
     # Set Application-id  
    CCA.appId=H.appId  
     # Set Hop-by-Hop and End-to-End from request  
    CCA.HopByHop=H.HopByHop  
    CCA.EndToEnd=H.EndToEnd  
     # Add AVPs to header and calculate remaining fields  
    ret=createRes(CCA,CCA_avps)  
     # ret now contains CCA Response as hex string     
    return ret   
def process_request(rawdata):  
  H=HDRItem()  
  stripHdr(H,rawdata)  
  dbg="Processing",dictCOMMANDcode2name(H.flags,H.cmd)  
  logging.info(dbg)  
  if H.flags & DIAMETER_HDR_REQUEST==0:  
    # If Answer no need to do anything  
    return SKIP  
  if H.cmd==257: # Capabilities-Exchange  
    return create_CEA(H)  
  if H.cmd==280: # Device-Watchdog  
    return create_DWA(H)  
  if H.cmd==272: # Credit-Control  
    return create_CCA(H)      
  if H.cmd==282: # Disconnect-Request-Peer  
    return create_DPA(H)  
  return create_UTC(H,"Unknown command code")  
def Quit():  
  for conn in sock_list:  
    conn.close()  
  sys.exit(0)  
if __name__ == "__main__":  
  # level for decoding are: DEBUG, INFO, WARNING, ERROR, CRITICAL  
  # logging.basicConfig(level=logging.INFO)  
  # Define server_host:port to use  
  HOST = "localhost"  
  DIAM_PORT = 3869  
  ORIGIN_HOST = "diameter.3gpp.org"  
  ORIGIN_REALM = "realm.3gpp.org"  
  DEST_REALM = "" # Leave it empty  
  LoadDictionary("dictDiameter.xml")  
  BUFFER_SIZE=1024    
  MAX_CLIENTS=5  
  sock_list=[]  
  # Create the server, binding to HOST:DIAM_PORT  
  OCS_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
  # fix "Address already in use" error upon restart  
  OCS_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  
  OCS_server.bind((HOST, DIAM_PORT))   
  OCS_server.listen(MAX_CLIENTS)  
  sock_list.append(OCS_server)  
  logging.info("Server started")  
  # Activate the server; this will keep running until you  
  # interrupt the program with Ctrl-C  
  while True:  
    try:  
      read, write, error = select.select(sock_list,[],[],1)  
    except:  
      break  
    for r in read:  
      logging.info("Incoming data")  
      # Is it new or existing connection  
      if r==OCS_server:  
        # New connections: accept on new socket  
        conn,addr=OCS_server.accept()  
        sock_list.append(conn)  
        if handle_OCS(conn)==ERROR:  
          Quit()  
      else:  
        if handle_OCS(r)==ERROR:  
          Quit()  
  Quit()
