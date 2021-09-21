from socket import *
import sys
"""
Command line argument: import sys sys.argv
sys.argv is a list,no need for split
"""

# In command promt the first argument is the IP address, 
# second is port and the third is filename
server_host = sys.argv[1]
server_port = sys.argv[2]
filename = sys.argv[3]

try:
	client_socket = socket(AF_INET,SOCK_STREAM)
    #Establish connection to server with IP address and port
	client_socket.connect((server_host,int(server_port))) 
    # Request file with HTTP GET request
	client_socket.send(('GET/HTTP/1.1 \r\n:%s\n\n' %(filename)).encode())

except IOError:
    # exit error 1 if connection could not be set up
    sys.exit(1)
    
# receive an encoded message from server and decode it
message=client_socket.recv(1024)
print (message.decode())
# continue receiving from server to retrieve the html file contents
while  True:
#for i in range (0, 50):
    message=client_socket.recv(1024)
    if message.decode() == "": break
    print (message.decode())
client_socket.close()