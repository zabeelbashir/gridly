import sys, ConfigParser

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
		def_flag = 0
		for line in self.lis:
			if '__main__' in line:
				self.func.append("def main():\n")
			else:
				if def_flag == 1:
					if '\t' not in line:
						def_flag = 0
						#self.func.append(line)
				if 'def ' in line:
					def_flag = 1
					self.func.append(line)
				if '\t' in line and def_flag == 1:
					self.func.append(line)

	def dump_file(self):
		Config = ConfigParser.ConfigParser()
		cfgfile = open("next.ini",'w')
		Config.add_section('DECLARATONS')
		final = ''
		for line in self.dec:
			final = line+final
		Config.set('DECLARATONS','String',''.join(self.dec).encode('string_escape'))
		Config.add_section('FUNCTIONS')
		Config.set('FUNCTIONS','String',''.join(self.func).encode('string_escape'))
		Config.add_section('CALL')
		Config.set('CALL', 'argument', False)
		Config.set('CALL', 'reference', False)
		Config.set('CALL', 'func_name', 'main')
		Config.set('CALL', 'return', False)
		Config.write(cfgfile)
		cfgfile.close()

obj = interprete()
obj.read_file()
print obj.lis
obj.extract_declarations()
print obj.dec
obj.extract_functions()
print obj.func
obj.main_extractor()
print obj.main
obj.dump_file()
