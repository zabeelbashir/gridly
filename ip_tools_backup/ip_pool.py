import threading
from ip_pool_publish import *
from ip_pool_query import *
from ip_pool_queue import *

class publish(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		a = ip_publish()
		a.ip_list_update()

class query(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		b = ip_query()
		b.ip_list_service_request()

def main():
	t0 = publish()
	t0.start()

	t1 = query()
	t1.start()

if __name__ == "__main__":
	main()
