from socket import *
import sys
"""
Command line argument: import sys sys.argv
sys.argv is a list,no need for split
"""
server_host = sys.argv[1]
server_port = sys.argv[2]
filename = sys.argv[3]

host_port = "%s:%s" %(server_host, server_port)
try:
	client_socket = socket(AF_INET,SOCK_STREAM)
	client_socket.connect((server_host,int(server_port)))
	client_socket.send(('GET / HTTP/1.1\r\nHost:%s\r\n\r\n' %(server_host)).encode())

except IOError:

	sys.exit(1)
message=client_socket.recv(1024)
client_socket.close()
print (message.decode())