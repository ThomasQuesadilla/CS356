#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 18 12:54:30 2021

@author: kyrachan
"""

#import socket module
from socket import *
import sys # In order to terminate the program

port = 4000;
serverSocket = socket(AF_INET, SOCK_STREAM)

#Prepare a server socket

# Bind to a particular port to receive connections on this port
serverSocket.bind(('', port));
# Listen for n = 1 connections on serverPort
serverSocket.listen(1)

while True:
    #Establish the connection
    print('Ready to serve...')
    
    #Set up and accept a new connection with the client
    connectionSocket, addr = serverSocket.accept()

    try:
        # Receive up to N = 1024 bytes from the connection socket
        message = connectionSocket.recv(1024);
        
        filename = message.split()[1]
        f = open(filename[1:])
        
        # Read data from file
        outputdata = f.read();
        
        #Send one HTTP header line into socket
        connectionSocket.send('HTTP/1.1 200 OK\n\n'.encode());
        
        #Send the content of the requested file to the client
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())
        
        connectionSocket.close()
    except IOError:
        #Send response message for file not found
        connectionSocket.send("HTTP/1.1 404 Not Found\n\n".encode())
        
        #Close client socket
        connectionSocket.close()
        
serverSocket.close()
sys.exit() #Terminate the program after sending the corresponding data