from socket import *
import sys
"""
Command line argument: import sys sys.argv
sys.argv is a list,no need for split
"""
server_host = sys.argv[1] # IP address is the first argument
server_port = sys.argv[2] # port is the second argument
filename = sys.argv[3] # filename is the third directory

try:
	client_socket = socket(AF_INET,SOCK_STREAM)
	client_socket.connect((server_host,int(server_port))) # connect to server
    # make header
 	header = {
 	"first_header" : "GET /%s HTTP/1.1" %(filename),
 	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
 	"Accept-Language": "en-us",
 	"Host": "%s:%s" %(server_host, server_port)
 	}
 	http_header = "\r\n".join("%s:%s" %(item,header[item]) for item in header)
 	print(http_header)
 	client_socket.send("%s\r\n\r\n" %(http_header))

except IOError:
	sys.exit(1)
final=""
message=client_socket.recv(1024)
# while response_message:
# 	final += response_message
# 	response_message = client_socket.recv(1024)

client_socket.close()
print (message.decode())
sys.exit()