#!/bin/sh
cd ..
#Disconnect-Peer
./tool_Diameter_decode.py 010000488000011a00000000000a0fa9000a91c10000010840000012737072696e742e636f6d00000000012840000012737072696e742e6e65740000000001114000000c00000000
read a
./tool_Diameter_decode.py 010000600000011a00000000000a0fa9000a91c10000010840000027636f726c6e782d656161613030322e65687270642e737072696e742e636f6d00000001284000001865687270642e737072696e742e636f6d0000010c4000000c000007d1
read a
