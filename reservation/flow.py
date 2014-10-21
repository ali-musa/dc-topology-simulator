import traffic
import path

class Flow(Traffic):
	def __init__(self, _id, _label, _start, _active, _rate, _size, _src, _dst):
		Traffic.__init__(self, _id, _label, _start, _active, _rate, _size)
		self.src = _src
		self.dst = _dst
		self.paths = []
