import time
from socket import *
import numpy as np

# Create a UDP socket
# Notice the use of SOCK_DGRAM for UDP packets
clientSocket = socket(AF_INET, SOCK_DGRAM)
# Set timeout to 2s / let client wait for up to 2s for a reply
clientSocket.settimeout(2.0)

message = ''
address = ('localhost', 12000)
times = []

# Send 15 pings to the server
for seqNum in range(1,16):
    # Measure the start time
    startTime = time.time()
    # Encode the message to send start time as well
    message = str(seqNum) + '\t' + str(startTime)
    if seqNum not in [4, 8, 12]:
        # The client sends the message to the server
        clientSocket.sendto(message.encode(), address)
        try:
            # Receive the server response
            response, server = clientSocket.recvfrom(1024)
            print(response)
        except Exception as e:
            print(e)
