#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 18 14:05:58 2021

@author: kyrachan
"""

# UDPPingerServer.py
# We will need the following modules to generate randomized lost packets
import time
from socket import *
import numpy as np

# Create a UDP socket
# Notice the use of SOCK_DGRAM for UDP packets
clientSocket = socket(AF_INET, SOCK_DGRAM)
# Set timeout to 2s / let client wait for up to 2s for a reply
clientSocket.settimeout(2.0)

message = 'ping'
address = ('localhost', 12000)
times = []

# Send 15 pings to the server
for seqNum in range(1,16):
    # Measure the start time
    startTime = time.time()
    
    # The server responds
    clientSocket.sendto(message.encode(), address)
    
    try:
        # Receive the client packet along with the address it is coming from
        response, server = clientSocket.recvfrom(1024)
        
        # Measure the end time
        endTime = time.time()
        
        # Calculate the RTT by subtracting the startTime from endTime
        RTT = endTime - startTime
        
        print('#%d'%seqNum)
        print('Response Message:%s'%response)
        print('RTT:%f seconds'%RTT)
        
        # Add RTTs to times array for later calculations
        times.append(float(RTT))
    
    # The server times out, no response
    except timeout:
        print('Request timed out')

# Statistics Calculations
print("Max time:%f" % max(times))
print("Min time:%f" % min(times))
print("Median time:%f" % np.median(times))
print("Average time:%f" % np.average(times))
print("Packet loss rate: %%%f" % ((15 - len(times))/15 * 100))
