import random
from socket import *
import time

# Create a UDP socket
# Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket(AF_INET, SOCK_DGRAM)
# Set timeout to 5s
serverSocket.settimeout(5.0)

# Assign IP address and port number to socket
serverSocket.bind(('localhost', 12000))
# Keep track of expected SeqNum to check for lost packets
expectedSeq = 1
# Keep track of the total number of lost packets
lostPackets = 0

while True:
    try:
        # Receive the client packet along with the address it is coming from
        message, address = serverSocket.recvfrom(1024)
        seqNumBytes, timestampBytes = message.split()
        
        # Decode seqNum
        seqNum = int(seqNumBytes)
        # Decode timestamp
        timestamp = float(str(timestampBytes)[2:-1])
        
        # Measure end time
        endTime = time.time()
        # Calculate time difference between time sent and time received
        timeDifference = endTime - timestamp
        
        # Check if seqNum matches to see if packet was lost
        if expectedSeq == seqNum:
            expectedSeq += 1
        else:
            lostPackets += 1
            expectedSeq = seqNum + 1
            
        # The server responds
        serverSocket.sendto(message, address)
        print('Packet received with sequence number %d\n
               Time difference: %f\n' % (seqNum, timeDifference))
               
   # The server times out, count total lost packets
    except timeout:
        print('Client application stopped.\nLost packets: %d' % lostPackets)
