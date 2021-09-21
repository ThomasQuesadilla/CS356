#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 18 14:05:58 2021

@author: kyrachan
"""

# UDPPingerServer.py
# We will need the following modules to generate randomized lost packets
import random
from socket import *
import time

# Create a UDP socket
# Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.settimeout(5.0)

# Assign IP address and port number to socket
serverSocket.bind(('localhost', 12000))
expectedSeq = 1
lostPackets = 0
while True:
    try:
        # Receive the client packet along with the address it is coming from
        message, address = serverSocket.recvfrom(1024)
        seqNumBytes, timestampBytes = message.split()
        seqNum = int(seqNumBytes)
        timestamp = float(str(timestampBytes)[2:-1])
        endTime = time.time()
        timeDifference = endTime - timestamp
        if expectedSeq == seqNum:
            expectedSeq += 1
        else:
            lostPackets += 1
            expectedSeq = seqNum + 1
        serverSocket.sendto(message, address)
        print('Packet received with sequence number %d\nTime difference: %f\n' % (seqNum, timeDifference))
    except timeout:
        print('Client application stopped.\nLost packets: %d' % lostPackets)
    
    # Otherwise, the server responds