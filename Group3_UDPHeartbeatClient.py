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
message = ''
address = ('localhost', 12000)

times = []

for seqNum in range(1,16):
    startTime = time.time()
    message = str(seqNum) + '\t' + str(startTime)
    if seqNum not in [4, 8, 12]:
        clientSocket.sendto(message.encode(), address)
        try:
            response, server = clientSocket.recvfrom(1024)
            print(response)
        except Exception as e:
            print(e)