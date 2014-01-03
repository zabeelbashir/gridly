import rpyc, ConfigParser, math

class task_management():

	def __init__(self):
		self.func = """
import psutil, time, os
def cpu_avg():
	cpu = 0
	x = 60
	for i in range(0, x):
		cpu += psutil.cpu_percent()
		time.sleep(1)
	return cpu / x
"""
		self.ip_list = ["192.168.1.28" , "127.0.0.1", "192.168.1.29"]
		self.cons = []
		self.routine_obj = []
		self.cpu_ret = []
	def start_sampling(self):
		i = 0
		for ip in self.ip_list:
			self.cons.append(rpyc.classic.connect( str(ip) ))
			self.cons[i].execute(self.func)
			self.function_namespace = self.cons[i].namespace["cpu_avg"]
			self.async_function = rpyc.async(self.function_namespace)
			self.async_routine = self.async_function()
			self.routine_obj.append(self.async_routine)
			i = i + 1

	def list_complete(self):
		print "Analysing your GRID"
		temp_list = [False] * len(self.ip_list)
		self.complete_list = [False] * len(self.ip_list)
		while False in self.complete_list:
			for key in range(0, len( self.ip_list )):
				if self.routine_obj[key].ready is True:
					if temp_list[key] is not True:
						self.cpu_ret.append(100-self.routine_obj[key].value)
						print "Analysis on " + str(self.ip_list[key]) + " is Completed!!!"
						temp_list[key] = True
						self.complete_list[key] = True

	def process_cpu(self):
		self.grid_power = sum(self.cpu_ret)
		self.contrib = [((x) / self.grid_power)*100  for (x) in self.cpu_ret]

	def task_get(self):
		self.lis = []
		self._file = open("task", "r")
		self.read_file = self._file.readlines()
		i = 0
		for line in self.read_file:
			self.lis.append(line)
			i = i + 1
		self.num_tasks = i

	def task_distributor(self):
		self.task_indv = []
		prev = 0
		for i in range(0, len(self.cpu_ret)):
			self.cpu_ret[i] = math.ceil((self.contrib[i]*self.num_tasks)/100)
		for i in range(0, len(self.cpu_ret)):
			self.task_indv.append(self.lis[prev:int(self.cpu_ret[i]+prev)])
			prev = int(self.cpu_ret[i])

	def task_dump(self):
		Config = ConfigParser.ConfigParser()
		cfgfile = open("temp.ini",'a')
		Config.add_section('TASKS')
		for task in range(0, len(self.task_indv)):
			Config.set('TASKS', self.ip_list[task],''.join(self.task_indv[task]).encode('string_escape'))
		Config.write(cfgfile)
		cfgfile.close()

	def _exit(self):
		for key in range(0, len( self.ip_list )):
			self.cons[key].close

if __name__ == "__main__":
	x = task_management()
	x.start_sampling()
	x.list_complete()
	x.process_cpu()
	x.task_get()
	x.task_distributor()
	x.task_dump()
