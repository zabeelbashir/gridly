import sys, ConfigParser
from thread_pool import *

class dispatch():

	def __init__(self):
		self.pool = thread_pool_manager()
		self.pool.exec_list_populate()
		self.pool.complete_list_populate()
		self.num_functions = 4
		self.pool.return_list_populate(self.num_functions)

	def declare_remote(self, function_string):
		for key in range(0, len( self.pool.ip_list )):
			self.pool.exec_list[key].async.declare(function_string)

	def _declare_remote(self, function_string, ip):
		self.pool.exec_list[self.pool.ip_list.index(ip)].async.declare(function_string)

	def execute_remote(self, key, function_name):
		self.pool.exec_list[key].async.async_function_(function_name)

	def execute_remote_with_arguments(self, key, function_name, argument):
		self.pool.exec_list[key].async.async_function_with_argument(function_name)

	def return_manager(self, key, func_ref):
		self.pool.return_list[key][func_ref] = self.pool.exec_list[key].async.async_routine.value

	def finally_manager(self, arguments, reference, func_name, val_return):
		for key in range(0, len( self.pool.ip_list )):
			if ('False' in arguments):
				self.execute_remote(key, func_name)
			if ('False' not in arguments):
				if reference == 'False':
					self.execute_remote_with_arguments(key, func_name, self.pool.return_list[key][int(reference)])
				else:
					self.execute_remote_with_arguments(key, func_name, arguments)
			if val_return == 'True':
				self.return_manager(key)

	def config_manager(self):
		Config = ConfigParser.ConfigParser()
		a = Config.read("temp.ini")
		sections = Config.sections()
		for ip in self.pool.ip_list:
			self._declare_remote("_TASKS="+str(Config.get('TASKS', ip).decode('string_escape').split('\n')), ip)
		for section in sections:
			if section == 'DECLARATONS' or section == 'FUNCTIONS':
				options = Config.options(section)
				for option in options:
					self.declare_remote(Config.get(section, option).decode('string_escape'))
			elif section == 'CALL':
				arg = Config.get(section, 'argument')
				ref = Config.get(section, 'reference')
				func_name = Config.get(section, 'func_name')
				ret = Config.get(section, 'return')
				self.finally_manager(arg, ref, func_name, ret)
				self.pool.list_complete()
		print "All Tasks Completed...Exiting now!"

if __name__ == "__main__":
	obj = dispatch()
	obj.config_manager()
