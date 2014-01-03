import time, socket
from ip_pool_queue import *
import multiprocessing

class ip_publish():
	def __init__(self):
		global queue
		queue = q_ip_pool()
                self.UDP_IP_PUBLISH="127.0.0.1"
                self.UDP_PORT_PUBLISH=10000
                self.sock_publish = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
		self.sock_publish.bind( (self.UDP_IP_PUBLISH,self.UDP_PORT_PUBLISH) )

	def ip_list_update(self):
		while True:
			data, addr = self.sock_publish.recvfrom( 1024 )
			print "received message:", data
			queue.put(data)

if __name__ == "__main__":
	init()
	while True:
		ip_list_update()
		print ip_get_list()
		time.sleep(5)
