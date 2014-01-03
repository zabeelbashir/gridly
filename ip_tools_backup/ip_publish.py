import socket

class ip_pool():
	def __init__(self):
		self.UDP_IP="192.168.1.21"
		self.UDP_PORT=5005
		self.sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
		self.sock.bind( (self.UDP_IP,self.UDP_PORT) )
		self.UDP_IP_LOCAL="127.0.0.1"
		self.UDP_PORT_LOCAL=10000
                self.sock_local = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )

	def data_get(self):
		while True:
			data, addr = self.sock.recvfrom( 1024 )
			print "received message:", addr[0]
			self.sock_local.sendto( addr[0], (self.UDP_IP_LOCAL, self.UDP_PORT_LOCAL) )

if __name__ == "__main__":
	pool = ip_pool()
	pool.data_get()
