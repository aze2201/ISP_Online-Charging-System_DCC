#!/usr/bin/python  
#############################################################################  
# Example of radius client sending Access-Request to IP:port of Radius server   
# This script is using pyprotosim software  
# Read the terms of BSD license at pyprotosim website:  
# http://sourceforge.net/projects/pyprotosim/    
############################################################################  
#Next two lines are to include parent directory for testing  
import sys  
sys.path.append("../")  
# Remove them normally  
# Radius client  
from libRadius import *  
import datetime  
import time  
def create_Request():  
  # Create message header (empty)  
  REQ=HDRItem()  
  # Set command code  
  REQ.Code=dictCOMMANDname2code("Access-Request")  
  REQ.Identifier=1  
  REQ.Authenticator=createAuthenticator()  
  # Let's build Request   
  REQ_avps=[]  
  REQ_avps.append(encodeAVP("Calling-Station-Id", "994704942025"))  
  REQ_avps.append(encodeAVP("Called-Station-Id", "test"))  
  REQ_avps.append(encodeAVP("User-Name", "994704942025"))  
  REQ_avps.append(encodeAVP("User-Password", PwCrypt(USER_PASSWORD,REQ.Authenticator,SECRET)))  
  REQ_avps.append(encodeAVP("NAS-Identifier", "GGSN"))  
  REQ_avps.append(encodeAVP("NAS-IP-Address", "1.2.3.4"))  
  REQ_avps.append(encodeAVP("NAS-Port-Type", 5))  
  REQ_avps.append(encodeAVP("NAS-Port", 6000))  
  REQ_avps.append(encodeAVP("Acct-Session-Id", "sessionID"))  
  REQ_avps.append(encodeAVP("Acct-Multi-Session-Id", "multisessionID"))  
  REQ_avps.append(encodeAVP("Service-Type", 2))  
  REQ_avps.append(encodeAVP("Framed-Protocol", 1))  
  # Add AVPs to header and calculate remaining fields  
  msg=createReq(REQ,REQ_avps)  
  # msg now contains Access-Request as hex string  
  return msg  
if __name__ == "__main__":  
  #logging.basicConfig(level=logging.DEBUG)  
  logging.basicConfig(level=logging.INFO)  
  LoadDictionary("dictRadius.xml")  
  HOST="127.0.0.1"  
  PORT=1812  
  USER_PASSWORD='password'  
  SECRET='SOMEPASSWORD'  
  # Let's assume that my Radius messages will fit into 4k  
  MSG_SIZE=4096  
  ###########################################################  
  Conn=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
  # socket is in blocking mode, so let's add a timeout  
  Conn.settimeout(5)  
  ###########################################################   
  # Create Access-Request    
  msg=create_Request()  
  # msg now contains Access-Request as hex string  
  logging.debug("+"*30)  
  #print "Access-Request",msg  
  # send data  
  Conn.sendto(msg.decode("hex"),(HOST,PORT))  
  # Receive response  
  received = Conn.recv(MSG_SIZE)  
  # Process response  
  RES=HDRItem()  
  stripHdr(RES,received.encode("hex"))  
  radius_avps=splitMsgAVPs(RES.msg)  
  for avps in radius_avps:  
    print decodeAVP(avps)  
  print radius_avps  
  # Normally - this is the end.  
  ###########################################################  
  # And close the connection  
  Conn.close()
