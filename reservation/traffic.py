import device

class Traffic:
	def __init__(self, _id, _label, _start, _active, _rate, _size):
		self.id = _id
		self.label = _label
		self.startTime = _start
		self.activeTime = _active
		self.endTime = _start + _active
		self.rate = _rate
		self.size = _size

# Utility functions
	def printInfo(self):
		print '=========================='
		print 'ID:       ' + str(self.id)
		print 'Label:    ' + str(self.label)
		print 'Rate:     ' + str(self.rate)
		print 'Size:     ' + str(self.size)
		print '=========================='