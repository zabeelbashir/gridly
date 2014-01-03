import socket
import sys

def get_file_data():
	_file = open("ips.ini", "r")
	_lines = _file.readlines()
	_lines = map(lambda s: s.strip(), _lines)
	return ','.join(_lines)

HOST = ''
PORT = 9999
try :
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	print 'Socket created'
except socket.error, msg :
	print 'Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
	sys.exit()
try:
	s.bind((HOST, PORT))
except socket.error , msg:
	print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
	sys.exit()
print 'Socket bind complete'
while 1:
	d = s.recvfrom(1024)
	data = d[0]
	addr = d[1]
	if not data: 
		break
	reply = 'OK...' + data
	s.sendto(get_file_data() , addr)
	print 'Message[' + addr[0] + ':' + str(addr[1]) + '] - ' + data.strip()
s.close()
