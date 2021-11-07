from socket import *
import os
import sys
import struct
import time
import select

ICMP_ECHO_REQUEST = 8
timeRTT = [] # list to accumulate RTTs
packageSent = 0 #counter for number of sent packages
packageReceived = 0 # counter for number of received packages

def checksum(string):
    csum = 0
    countTo = (len(string) // 2) * 2
    count = 0
    while count < countTo:
        thisVal = string[count + 1] * 256 + string[count]
        csum = csum + thisVal
        csum = csum & 0xffffffff
        count = count + 2
    if countTo < len(string):
        csum = csum + ord(string[len(string) - 1])
        csum = csum & 0xffffffff
    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer


def receiveOnePing(mySocket, ID, timeout, destAddr):
    global packageReceived, timeRTT
    timeLeft = timeout
    while 1:
        startedSelect = time.time()
        whatReady = select.select([mySocket], [], [], timeLeft)
        howLongInSelect = (time.time() - startedSelect)
        if whatReady[0] == []: # Timeout - if packet is empty
             return "Destination Network Unreachable"
        timeReceived = time.time()
        recPacket, addr = mySocket.recvfrom(1024)
 # Fill in start
 # Fetch the ICMP header from the IP packet
        icmpHeader = recPacket[20:28]
        icmpType, icmpCode, icmpChecksum, icmpPacketID, icmpSequence = struct.unpack("bbHHh", icmpHeader)

        # Decomposition of error codes
        if icmpType != 0:
            if icmpType == 3:
                if icmpCode == 0:
                    return "Destination Network Unreachable"
                elif icmpCode == 1:
                    return "Destination Host Unreachable"
                elif icmpCode == 2:
                    return "Destination Protocol Unreachable"
            else:
                return "Other Errors"

        # If correct packet is received
        if icmpPacketID == ID:
            # Calculate byte size of timestamp data
            bytesInDouble = struct.calcsize("d")
            timeSent = struct.unpack("d", recPacket[28:28 + bytesInDouble])[0]
            timeRTT.append(timeReceived - timeSent) # append RTT time to the list
            packageReceived = packageReceived+1 #increase number of received packages by 1
            return timeReceived - timeSent

        timeLeft = timeLeft - howLongInSelect
       
        if timeLeft <= 0:
           return "Request timed out."
 # Explain each line
 # Fill in end
 
 
def sendOnePing(mySocket, destAddr, ID):
    global packageSent, timeRTT
    # Header is type (8), code (8), checksum (16), id (16), sequence (16)
    myChecksum = 0
    
    # Make a dummy header with a 0 checksum
    
    # struct -- Interpret strings as packed binary data
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    data = struct.pack("d", time.time())
    # Calculate the checksum on the data and the dummy header.
    myChecksum = checksum(header + data)
    
    # Get the right checksum, and put in the header
    if sys.platform == 'darwin':
        # Convert 16-bit integers from host to network byte order
        myChecksum = htons(myChecksum) & 0xffff
    else:
        myChecksum = htons(myChecksum)
        
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    packet = header + data
    
    mySocket.sendto(packet, (destAddr, 1)) # AF_INET address must be tuple, not str
    packageSent=packageSent+1 #increase number of sent packages by 1
    # Both LISTS and TUPLES consist of a number of objects
    # which can be referenced by their position number within the object.
    
def doOnePing(destAddr, timeout):
    icmp = getprotobyname("icmp")
        # SOCK_RAW is a powerful socket type. For more details: http://sockraw.org/papers/sock_raw
 
    mySocket = socket(AF_INET, SOCK_RAW, icmp)
    
    myID = os.getpid() & 0xFFFF # Return the current process i
    sendOnePing(mySocket, destAddr, myID)
    delay = receiveOnePing(mySocket, myID, timeout, destAddr)
    
    mySocket.close()
    return delay


def ping(host, timeout=1):
 # timeout=1 means: If one second goes by without a reply from the server,
 # the client assumes that either the client's ping or the server's pong is lost
     dest = "128.119.8.148"
     print("Pinging " + dest + " using Python:")
     print("")
     # Send ping requests to a server separated by approximately one second
     while 1:
         delay = doOnePing(dest, timeout)
         print("RTT: ",delay)
         if (len(timeRTT)>0):
             print("maxRTT: ", max(timeRTT)) #max of the list
             print("minRTT: ", min(timeRTT)) #min of the list
             print("averageRTT: ", float(sum(timeRTT)/len(timeRTT))); #average of all RTTs
             print("Package loss rate: ", (packageSent - packageReceived)/packageSent) #average rate of package loss
         else:
             print("maxRTT: ", 0)
             print("minRTT: ", 0)   
             print("averageRTT: ", 0)
             print("average loss rate:", 0)
         time.sleep(1) # one second return delay
         
#ping("umass.edu")
#ping("alibaba.com")
#ping("bbc.com")
#ping("unimelb.edu.au")
ping("pretoriazoo.org")
