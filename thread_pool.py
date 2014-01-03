import sys, socket
from exec_class import *

class thread_pool_manager():

	def __init__(self):
		self.UDP_IP_QUERY_OUT="127.0.0.1"
		self.UDP_PORT_QUERY_OUT=10001
		self.sock_query_out = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
		self.UDP_IP_QUERY_IN="127.0.0.1"
		self.UDP_PORT_QUERY_IN=10002
		self.sock_query_in = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
		self.sock_query_in.bind( (self.UDP_IP_QUERY_IN,self.UDP_PORT_QUERY_IN) )
		self.ip_list = ["192.168.1.28", "192.168.1.29" , "127.0.0.1"]
		self.exec_list = []
		self.complete_list = []
		self.return_list = []

	def get_ip_pool(self):
		self.sock_query_out.sendto( "IP_LIST_QUERY", (self.UDP_IP_QUERY_OUT, self.UDP_PORT_QUERY_OUT) )
		iplist, addr = self.sock_query_in.recvfrom( 1024 )
		self.ip_list = iplist.split(",")

	def exec_list_populate(self):
		for ip in self.ip_list:
			self.exec_list.append(remote_operation(ip))

	def complete_list_populate(self):
		self.complete_list = [False] * len(self.ip_list)

	def return_list_populate(self, num_func):
		for i in range(0, len(self.ip_list)):
			self.return_list.append([0] * num_func)

	def list_complete(self):
		print "Waiting for Task Completion"
		temp_list = [False] * len(self.ip_list)
		while False in self.complete_list:
			for key in range(0, len( self.ip_list )):
				if self.pool_status(key) is True:
					if temp_list[key] is not True:
						self.complete_list[key] = True
						print "Task Processing on " + str(self.ip_list[key]) + " is Completed!!!"
						temp_list[key] = True
					else:
						pass
				else:
					pass

	def pool_status(self, key):
		if self.exec_list[key].async.async_routine.ready is True:
			return True
		elif self.exec_list[key].async.async_routine.ready is False:
			return False

	def update_list():
		self.get_ip_pool()
	
	def test(self):
		""" ONLY FOR TESTING PURPOSES """
		for key in range(0, len(self.ip_list)):
			print self.exec_list[key].async.id
			print self.exec_list[key].sync.id

if __name__ == "__main__":
	a = thread_pool_manager()
	a.exec_list_populate()
	a.callback_list_populate()
	a.test()
