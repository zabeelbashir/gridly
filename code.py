import sys,urllib
print "zabeel rocks"
_TASKS=[]
def test(x):
	print "hello form the grid"
	print x * 107
	return x * 107

def temp(y):
	print "temp function in the grid. the element is: " + str(y)
	print _TASKS
	return y/10

if __name__ == "__main__":
	a = test(87)
	b = temp(a)
	print "final value is: " + str(b)
