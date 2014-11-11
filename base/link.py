from component import Component
from enum import *

class Link(Component):
	def __init__(self, _id, _label, _cap, _device1, _device2):
		Component.__init__(self, _id, _label)
		self.compType = CompType.LINK
		self.totalCap = _cap
		self.capAB = _cap
		self.capBA = _cap
		self.deviceA = _device1
		self.deviceB = _device2

# over-loaded __str__() for print functionality
	def __str__(self):
		printString =  "=========================="
		printString += "\nLink Information"
		printString += "\n--------------------------"
		printString += "\nID:       " + str(self.id)
		printString += "\nLabel:    " + str(self.label)
		printString += "\nStatus:   " + str(self.status)
		# printString += "\nDevice A: " + str(self.deviceA)
		# printString += "\nDevice B: " + str(self.deviceB)
		printString += "\nCapacity: " + str(self.totalCap)
		printString += "\nAB Cap:   " + str(self.capAB)
		printString += "\nBA Cap:   " + str(self.capBA)
		printString += "\n=========================="
		return printString

# Setter functions
	def setBW(self, _bw, device):
		if device == self.deviceA:
			self.capAB -= _bw
		if device == self.deviceB:
			self.capBA -= _bw

	def setBW_AB(self, _bw):
		self.capAB -= _bw

	def setBW_BA(self, _bw):
		self.capBA -= _bw

# Getter functions
	def getAvailableBW(self, device):
		if device == self.deviceA:
			return self.capAB
		if device == self.deviceB:
			return self.capBA

	def getDevice_A(self):
		return self.deviceA

	def getDevice_B(self):
		return self.deviceB

	def getOtherDevice(self, _device):
		if self.deviceA == _device:
			return self.deviceB
		if self.deviceB == _device:
			return self.deviceA