class Traffic:
	def __init__(self, _id, _label, _time, _active, _bw):
		self.id = _id
		self.label = _label
		self.time = _time
		self.activeTime = _active
		self.endTime = _time + _active
		self.bw = _bw

# Utility functions
	def printInfo(self):
		print '=========================='
		print 'ID:       ' + str(self.id)
		print 'Label:    ' + str(self.label)
		print 'Time:	 ' + str(self.time)
		print 'Rate:     ' + str(self.bw)
		print '=========================='