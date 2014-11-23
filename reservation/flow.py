import sys, os.path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from traffic import Traffic
from base.enum import *
from base.path import Path

class Flow(Traffic):
	def __init__(self, _label, _time, _active, _bw, _src, _dst):
		Traffic.__init__(self, _label, _time, _active, _bw)
		self.src = _src
		self.dst = _dst
		self.paths = []

	def addPath(self, path):
		self.paths.append(path)

		length = path.getLength()
		comps = path.getComponents()
		for i in range(length):
			if comps[i].getType() == CompType.LINK:
				comps[i].reserveBW(self.bw, comps[i-1])
