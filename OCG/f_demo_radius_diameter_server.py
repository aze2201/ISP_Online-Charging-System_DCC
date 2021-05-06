#!/usr/bin/python  
#################################################################################################  
# Example of radius server sending diameter Credit-Control requests to IP:port of Diameter server   
# This script is using pyprotosim software  
# Read the terms of BSD license at pyprotosim website:  
# http://sourceforge.net/projects/pyprotosim/    
################################################################################################  
import sys  
#Next line is to include parent directory in PATH where libraries are  
sys.path.append("../")  
from libRadius import *  
import libDiameter  
import datetime  
# Function to create diameter CCR request and parse received CCA response from Diameter server  
def send_ccr_i(identity):  
 IDENTITY=identity  
 CCR_avps=[ ]  
 CCR_avps.append(libDiameter.encodeAVP('Origin-Host', ORIGIN_HOST))   
 CCR_avps.append(libDiameter.encodeAVP('Session-Id', GY_SESSIONID))  
 CCR_avps.append(libDiameter.encodeAVP('Called-Station-Id', 'test.apn'))  
 CCR_avps.append(libDiameter.encodeAVP('Origin-Realm', ORIGIN_REALM))  
 CCR_avps.append(libDiameter.encodeAVP('Destination-Realm', DEST_REALM))  
 CCR_avps.append(libDiameter.encodeAVP('Destination-Host', DEST_HOST))  
 CCR_avps.append(libDiameter.encodeAVP('Auth-Application-Id', 4))  
 CCR_avps.append(libDiameter.encodeAVP('CC-Request-Type', 1))  
 CCR_avps.append(libDiameter.encodeAVP('CC-Request-Number', 0))  
 CCR_avps.append(libDiameter.encodeAVP('Subscription-Id',[libDiameter.encodeAVP('Subscription-Id-Data', IDENTITY ), libDiameter.encodeAVP('Subscription-Id-Type', 1)]))  
 CCR_avps.append(libDiameter.encodeAVP('3GPP-SGSN-Address', '192.168.0.2'))  
 CCR_avps.append(libDiameter.encodeAVP('3GPP-MS-TimeZone', 'GMT'))  
 CCR_avps.append(libDiameter.encodeAVP('Access-Network-Charging-Address', '192.168.0.2'))  
 # Create message header (empty)  
 CCR=libDiameter.HDRItem()  
 # Set command code  
 CCR.cmd=libDiameter.dictCOMMANDname2code('Credit-Control')  
 # Set Hop-by-Hop and End-to-End  
 libDiameter.initializeHops(CCR)  
 # Add AVPs to header and calculate remaining fields  
 msg1=libDiameter.createReq(CCR,CCR_avps)  
 # msg now contains CCR Request as hex string  
 # send data  
 Conn=libDiameter.Connect(OCS_HOST,OCS_PORT)  
 Conn.send(msg1.decode('hex'))  
 # Receive response  
 received1 = Conn.recv(1024)  
 # Parse and display received ANSWER  
 #print "="*30  
 #print "THE CCA - I ANSWER IS:"  
 msg=received1.encode('hex')  
 #print "="*30  
 H=libDiameter.HDRItem()  
 libDiameter.stripHdr(H,msg)  
 CCA_avps=libDiameter.splitMsgAVPs(H.msg)  
 cmd=libDiameter.dictCOMMANDcode2name(H.flags,H.cmd)  
 # We need get STATE 2001 or 5003 from Response  
 CCA_status=libDiameter.findAVP("Result-Code",CCA_avps)  
 if str(CCA_status) in ['2001']:   
  return True  
 elif str(CCA_status) in ['5003','5002']:   
  return False  
 else:  
  return False  
# Function that creates radius access response to the client
valid_user=''
def create_Access_Response():  
 # Create message header (empty)  
 RES=HDRItem()  
 stripHdr(RES,data.encode("hex"))  
 RID=RES.Identifier  
 RES.Code=dictCOMMANDname2code("Access-Request")  
 RES.Identifier=RID  
 REQ_avps=splitMsgAVPs(RES.msg)  
 try:  
  IDENTITY=findAVP("Calling-Station-Id",REQ_avps)  
  USER_NAME=findAVP("User-Name",REQ_avps)  
  enc_password=findAVP("User-Password",REQ_avps)  
  #USER_PASS_DECODED=PwDecrypt(enc_password,RES.Authenticator.decode("hex"),SECRET)  
  USER_PASS_DECODED='password'
 except:  
  pass  
 print "Found user identity is", str(IDENTITY)  
 print "Received Accounting Access Request from User" + ":"+str(USER_NAME) +","+ "and Password is " + str(USER_PASS_DECODED)  
 if USER_NAME == 'test' and USER_PASS_DECODED == 'password':  
 #Call DIAMETER with IDENTITY as CCR-I  
  valid_user=send_ccr_i(IDENTITY)  
 #This will be Access-Accept returned to client  
 if valid_user is True:  
  RES.Code=dictCOMMANDname2code("Access-Accept")  
  RES_avps=[]  
  auth=createAuthenticator()  
  RES_avps.append(encodeAVP('Session-Timeout',600 ))  
  RES_avps.append(encodeAVP('Acct-Interim-Interval', 60))  
  msg=createWithAuthenticator(RES,auth,RES_avps,SECRET)  
  return msg  
 elif valid_user is False:  
 #This will be Access-Reject returned to client  
  RES.Code=dictCOMMANDname2code("Access-Reject")  
  RES_avps=[]  
  auth=createAuthenticator()  
  msg=createWithAuthenticator(RES,auth,RES_avps,SECRET)  
  return msg   
 else:  
 # This will be Access-Reject too  
  RES.Code=dictCOMMANDname2code("Access-Reject")  
  RES_avps=[]  
  auth=createAuthenticator()  
  msg=createWithAuthenticator(RES,auth,RES_avps,SECRET)  
  return msg  
def create_Session_Id():  
  #The Session-Id MUST be globally and eternally unique  
  #<DiameterIdentity>;<high 32 bits>;<low 32 bits>[;<optional value>]  
  now=datetime.datetime.now()  
  ret=ORIGIN_HOST+";"  
  ret=ret+str(now.year)[2:4]+"%02d"%now.month+"%02d"%now.day  
  ret=ret+"%02d"%now.hour+"%02d"%now.minute+";"  
  ret=ret+"%02d"%now.second+str(now.microsecond)  
  return ret  
if __name__ == "__main__":  
 logging.basicConfig(level=logging.DEBUG)  
 #logging.basicConfig(level=logging.INFO)  
 LoadDictionary("dictRadius.xml")  
 libDiameter.LoadDictionary("dictDiameter.xml")  
 # Set up here IP and Port for your RADIUS ACCOUNTING server  
 RADIUS_IP = "localhost"  
 RADIUS_PORT = 1812  
 BUFFER_SIZE=4096  
 # Set up shared secret here  
 SECRET="SOMEPASSWORD"  
 # FOR OCS SERVER:  
 OCS_HOST="3bash.com"  
 OCS_PORT=3868  
 ORIGIN_HOST="radius.3gpp.org"  
 ORIGIN_REALM="realm.3gpp.org"  
 DEST_REALM="realm.3gpp.org"  
 DEST_HOST="diameter.3gpp.org"  
 GY_SESSIONID=create_Session_Id()  
 # Now creating simple udp socket   
 RADIUS_server = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)  
 RADIUS_server.bind((RADIUS_IP, RADIUS_PORT))  
 # Starting udp server in a loop  
 # Looping server until user sends CTRL+C or kill to stop it.  
 while True:  
  data, addr = RADIUS_server.recvfrom(BUFFER_SIZE)  
  if (data != ""):   
   msg=create_Access_Response()  
   dbg="Sending Access Response"  
   logging.info(dbg)  
   RADIUS_server.sendto(msg.decode("hex"),addr)
   #END of code