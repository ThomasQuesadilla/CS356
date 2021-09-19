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


clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(2.0)
message = 'ping'
address = ('localhost', 12000)

for seqNum in range(1,16):
    startTime = time.time()
    clientSocket.sendto(message.encode(), address)
    try:
        response, server = clientSocket.recvfrom(1024)
        endTime = time.time()
        RTT = endTime - startTime
        print('#%d'%seqNum)
        print('Response Message:%s'%response)
        print('RTT:%fseconds'%RTT)
    except timeout:
        print('Request timed out')