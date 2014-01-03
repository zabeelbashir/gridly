import web
import rpyc

def make_text(string):
    return string

urls = ('/', 'tutorial')
render = web.template.render('templates/')

app = web.application(urls, globals())

my_form = web.form.Form(web.form.Textbox('', class_='textfield', id='textfield'),)

class tutorial:

	def __init__(self):
		self.ip_list = ["192.168.1.28" , "127.0.0.1"]
		print self.ip_list
		self.data = []
		self.data_obj = {'cpu': '' , 'ram' : ''}
		self.connection_list = []

	def conn_manager(self):
		for ip in self.ip_list:
			self.connection_list.append(rpyc.classic.connect( str(ip)))

	def get_values(self):
		for connection in (0, len(self.connection_list)-1):
			self.data_obj['cpu'] = str(self.connection_list[connection].modules.psutil.cpu_percent())
			self.data_obj['ram'] = (str( self.connection_list[connection].modules.psutil.phymem_usage() ).strip("usage()").split(","))[3].strip(" percentage=")
			self.data.append(self.data_obj)
		print self.data

	def GET(self):
		form = my_form()
		return render.tutorial(form, "Your text goes here.")
        
	def POST(self):
		self.conn_manager()
		self.get_values()
		form = my_form()
		form.validates()
		s = form.value['textfield']
		print s
		return make_text(str(self.data))

if __name__ == '__main__':
	app.run()
