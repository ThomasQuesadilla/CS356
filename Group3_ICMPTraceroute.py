from socket import *
import os
import sys
import struct
import time
import select

ICMP_ECHO_REQUEST = 8
MAX_HOPS = 30
TIMEOUT = 2.0
TRIES = 2

# The packet that we shall send to each router along the path is the ICMP echo
# request packet, which is exactly what we had used in the ICMP ping exercise.
# We shall use the same packet that we built in the Ping exercise
def checksum(string):
    # In this function we make the checksum of our packet
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

def build_packet():
    # In the sendOnePing() method of the ICMP Ping exercise ,firstly the header of our
    # packet to be sent was made, secondly the checksum was appended to the header and
    # then finally the complete packet was sent to the destination.

    #Fill in start

    # Make the header in a similar way to the ping exercise.
    # Start checksum at 0
    myChecksum = 0
    # gets ID of client
    myID = os.getpid() & 0xFFFF

    # Makes a dummy header with 0 as checksum
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, myID, 1)
    # Packs timestamp data into struct
    data = struct.pack("d", time.time())
    # Append checksum to the header.
    # Don’t send the packet yet, just return the final packet in this function.


    # Calculates checksum on data and dummy header.
    myChecksum = checksum(header + data)

    # Get right checksum based on platform
    if sys.platform == 'darwin':
        # Convert 16-bit integers from host to network byte order
        myChecksum = htons(myChecksum) & 0xffff

    else:
        myChecksum = htons(myChecksum)

    # Creates header with real checksum
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, myID, 1)
    #Fill in end

    packet = header + data
    return packet

def get_route(hostname):
    timeLeft = TIMEOUT
    for ttl in range(1, MAX_HOPS):
        for tries in range(TRIES):
            destAddr = gethostbyname(hostname)
            # Fill in start
            # Sets up type of protocol to initialize socket
            icmp = getprotobyname("icmp")
            # Initializes socket
            mySocket = socket(AF_INET, SOCK_RAW, icmp)
            # Fill in end

            mySocket.setsockopt(IPPROTO_IP, IP_TTL, struct.pack('I', ttl))
            mySocket.settimeout(TIMEOUT)

            try:
                d = build_packet()
                mySocket.sendto(d, (hostname, 0))
                t = time.time()
                startedSelect = time.time()
                whatReady = select.select([mySocket], [], [], timeLeft)
                howLongInSelect = (time.time() - startedSelect)

                if whatReady[0] == []: 
                    print(" * * * Request timed out.")
                recvPacket, addr = mySocket.recvfrom(1024)
                timeReceived = time.time()
                timeLeft = timeLeft - howLongInSelect

                if timeLeft <= 0:
                    print(" * * * Request timed out.")

            except timeout:
                continue

            else:
                # Fill in start
                # Fetch the icmp type from the IP packet
                icmpHeader = recvPacket[20:28]
                ICMPType, Code, myChecksum, myID, sequence = struct.unpack("bbHHh", icmpHeader)
                #Fill in end

                if ICMPType == 11:
                    bytes = struct.calcsize("d")
                    timeSent = struct.unpack("d", recvPacket[28:28 +bytes])[0]
                    print(" %d rtt=%.0f ms %s" % (ttl,(timeReceived - t) * 1000, addr[0]))

                elif ICMPType == 3:
                    bytes = struct.calcsize("d")
                    timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
                    print(" %d rtt=%.0f ms %s" % (ttl,(timeReceived - t) * 1000, addr[0]))

                elif ICMPType == 0:
                    bytes = struct.calcsize("d")
                    timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
                    print(" %d rtt=%.0f ms %s" % (ttl, (timeReceived - timeSent) * 1000, addr[0]))
                    return

                else:
                    print("error")
                    break

            finally:
                mySocket.close()

print("--------------------------------------------")
print ("umass.edu")
get_route("umass.edu")
print("--------------------------------------------")
print ("alibaba.com")
get_route("alibaba.com")
print("--------------------------------------------")
print ("bbc.com")
get_route("bbc.com")
print("--------------------------------------------")
print ("unimelb.edu.au")
get_route("unimelb.edu.au")
print("--------------------------------------------")
print ("pretoriazoo.org")
get_route("pretoriazoo.org")