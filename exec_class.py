import rpyc

class exec_remote():

	class sync():

		def __init__(self, conn):
			self.conn = conn
			self.id = "Test form sync with conn object: " + str(self.conn)

		def declare(self, function_string):
			self.conn.execute(function_string)

		def sync_function(self, function, function_name, argument):
			self.conn.execute(function)
			self.conn.namespace[function_name](argument)

		def sync_function_with_sdio(self, function, function_name, argument):
			self.conn.execute(function)
			with rpyc.classic.redirected_stdio(conn):
				self.conn.namespace[function_name](argument)

		def remote_map(self, function_pointer, param_list):
			self.conn.modules.__builtin__.map(function_pointer, param_list)

	class async():

		def __init__(self, conn):
			self.conn = conn
			self.async_routine = None
			self.async_function = None
			self.id = "Test form async with conn object: " + str(self.conn)

		def pool_ready(self):
			if self.async_routine.ready is True:
				return True
			elif self.async_routine.ready is False:
				return False

		def declare(self, function_string):
			self.conn.execute(function_string)

		def async_function_with_callback(self, function_string, function_name, argument, callback):
			self.conn.execute(function_string)
			self.function_namespace = conn.namespace[function_name]
			self.async_function = rpyc.async(self.function_namespace)
			self.async_routine = self.async_function(argument)
			self.async_routine.add_callback(callback)
			self.async_routine.wait()
			self.async_routine.value

		def async_function_(self, function_name):
			self.function_namespace = eval('self.conn.namespace[function_name]')
			self.async_function = rpyc.async(self.function_namespace)
			self.async_routine = self.async_function()

		def test(self):
			print "this is working fine now"

		def async_function_with_argument(self, function_name, argument):
			self.function_namespace = self.conn.namespace[function_name]
			self.async_function = rpyc.async(self.function_namespace)
			self.async_routine = self.async_function(argument)
			self.async_routine.wait()
			self.async_routine.value

		def async_module(self, module_name):
			self.remote_module = rpyc.async(self.conn.modules.time.sleep)


class remote_operation():
	def __init__(self, ip):
			self.conn = rpyc.classic.connect( str(ip) )
			self.test_obj = exec_remote()
			self.sync = self.test_obj.sync(self.conn)
			self.async = self.test_obj.async(self.conn)

def testing(value):
	print "hello world"

hello_txt = """
import socket
def hello(a):
	import os
	print "Hello from", os.getcwd()
	print "arg: " + str(a)
"""

if __name__ == "__main__":
	test_obj = exec_remote("192.168.2.107")
	sync_test_obj = test_obj.sync()
	sync_test_obj.remote_execute_function(hello_txt, 'hello', 1921)
	sync_test_obj.remote_execute_function_with_sdio(hello_txt, 'hello', 10098)
	
	async_test_obj = test_obj.async()
	async_test_obj.async_function_with_callback(hello_txt, 'hello', 1234, testing)
	async_test_obj.async_module("abc")
	conn.close()
