

class interprete():
	def __init__(self):
		print "starting interpreting"
		self.lis = []
		self.dec = []
		self.func = []
		self.main = []
		self.main_final = []
		self.func_name = []
		self.main_dict = { 'argument' : '' , 'reference' : '' , '_return' :'' , 'func_name' : '' }
		self.ref = []
		self.ref_temp = []
		self.ret =[]

	def read_file(self):
		self._file = open ('code.py', 'r')
		self.read_file = self._file.readlines()
		for line in self.read_file:
			self.lis.append(line)
			if '\n' in self.lis:
				self.lis.remove('\n')

	def extract_declarations(self):
		for line in self.lis:
			if '\t' in line:
				pass
			else:
				if '__main__' not in line and 'def ' not in line:
					self.dec.append(line)

	def extract_functions(self):
		temp = []
		def_flag = 0
		for line in self.lis:
			if def_flag == 1:
				if '\t' not in line:
					def_flag = 0
					self.func.append(temp)
					temp = []
			if 'def ' in line:
				def_flag = 1
				temp.append(line)
			if '\t' in line and def_flag == 1:
				temp.append(line)

	def main_extractor(self):
		main_flag = 0
		temp = []
		for line in self.lis:
			if main_flag == 1:
				if '\t' not in line:
					main_flag = 0
					temp = []
			if '__main__' in line:
				main_flag = 1
			if '\t' in line and main_flag == 1:
				self.main.append(line)

	def main_manager(self):
		for line in self.func:
			self.func_name.append(self.extract_name(line))
			self.ret.append(self._ret(line))
		for line in self.main:
			self.ref.append(self.extract_reference(line))

	def extract_name(self, lines):
		for line in lines:
			if 'def ' in line:
				return (line.strip('\ndef ')).strip('():')

	def extract_reference(self, line):
		line_ref = line.strip('\n\t')
		line = line.strip('\n\t')
		print line
		if '=' in line:
			for name in self.func_name:
				if name in line:
					print name
					line = line.strip('()')
					line = line.strip(name)
					line = line.strip(' = ')
					self.ref_temp.append(line)
		else:
			if '('+ line +')' in line_ref:
				print 'found reference'
			self.ref_temp.append(False)

	def arguments_manage(self, line):
		pass

	def _ret(self, line):
		if 'return' in line:
			return True
		else:
			return False

	def dump_file(self):
		pass

obj = interprete()
obj.read_file()
print obj.lis
obj.extract_declarations()
print obj.dec
obj.extract_functions()
print obj.func
obj.main_extractor()
obj.main_manager()
#print obj.main
