from ip_pool_queue import *
import socket
import multiprocessing

class ip_query():
	def __init__(self):
		global queue
		queue = q_ip_pool()
                self.UDP_IP_QUERY_IN="127.0.0.1"
                self.UDP_PORT_QUERY_IN=10001
                self.sock_query_in = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
		self.sock_query_in.bind( (self.UDP_IP_QUERY_IN,self.UDP_PORT_QUERY_IN) )
                self.UDP_IP_QUERY_OUT="127.0.0.1"
                self.UDP_PORT_QUERY_OUT=10002
                self.sock_query_out = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
		self.ip_list = []

	def ip_list_update(self):
		if queue.is_empty() is True:
			pass
		else:
			ip = queue.get()
			if self.check_duplicate(ip) is True:			
				self.ip_list.append(ip)
				print self.ip_list
			else:
				print "duplicate"

	def ip_list_service_request(self):
		while True:
			data, addr = self.sock_query_in.recvfrom( 1024 )
			print "received message:", data
			self.ip_list_update()
			self.sock_query_out.sendto( ",".join(self.ip_list), (self.UDP_IP_QUERY_OUT, self.UDP_PORT_QUERY_OUT) )

	def check_duplicate(self, ip):
		if ip in self.ip_list:
			return False
		else:
			return True
