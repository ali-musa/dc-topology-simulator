import uuid
class Traffic:
	def __init__(self, _label, _time, _active, _bw):
		self.id = uuid.uuid4()
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

# Getter functions
	def getID(self):
		return self.id
