import socket
    
UDP_IP="127.0.0.1"
UDP_PORT=10001
MESSAGE="IP_QUERY"
    
print "UDP target IP:", UDP_IP
print "UDP target port:", UDP_PORT
print "message:", MESSAGE

sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM ) # UDP
sock.sendto( MESSAGE, (UDP_IP, UDP_PORT) )


sock.close()
