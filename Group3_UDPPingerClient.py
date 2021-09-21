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


clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(2.0)
message = 'ping'
address = ('localhost', 12000)
times = []

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
        times.append(float(RTT))
    except timeout:
        print('Request timed out')

print("Max time:%f" % max(times))
print("Min time:%f" % min(times))
print("Median time:%f" % np.median(times))
print("Average time:%f" % np.average(times))
print("Packet loss rate: %%%f" % ((15 - len(times))/15 * 100))