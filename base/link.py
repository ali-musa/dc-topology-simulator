from component import Component
from enum import *

class Link(Component):
	def __init__(self, _id, _label, _cap, _device1, _device2):
		Component.__init__(self, _id, _label)
		self.compType = CompType.LINK
		self.totalCapacity = _cap
		self.capacityAvailableAB = _cap
		self.capacityAvailableBA = _cap
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
		printString += "\nCapacity: " + str(self.totalCapacity)
		printString += "\nAB Cap:   " + str(self.capacityAvailableAB)
		printString += "\nBA Cap:   " + str(self.capacityAvailableBA)
		printString += "\n=========================="
		return printString

# Setter functions
	def reserveBandwidth(self,bandwidth): #reserve equally on both directions
		self.capacityAvailableAB -=bandwidth
		self.capacityAvailableBA -=bandwidth
		assert(0<=self.capacityAvailableAB<=self.totalCapacity)
		assert(0<=self.capacityAvailableBA<=self.totalCapacity)

	def reserveBWFromDevice(self, _bw, device):
		if device == self.deviceA:
			if(self.capacityAvailableAB - _bw >= 0):
				self.capacityAvailableAB -= _bw
			else:
				x = 1/0
			# assert(self.capAB >= 0)
		if device == self.deviceB:
			if(self.capacityAvailableBA - _bw >= 0):
				self.capacityAvailableBA -= _bw
			else:
				x = 1/0
			# assert(self.capBA >= 0)

	def reserveBW_AB(self, _bw):
		if(self.capacityAvailableAB - _bw >= 0):
			self.capacityAvailableAB -= _bw
		else:
			x = 1/0
		# self.capAB -= _bw
		# assert(self.capAB >= 0)

	def reserveBW_BA(self, _bw):
		if(self.capacityAvailableBA - _bw >= 0):
			self.capacityAvailableBA -= _bw
		else:
			x = 1/0
		# self.capBA -= _bw
		# assert(self.capBA >= 0)

	def unReserveBandwidth(self,bandwidth): #un-reserve equally on both directions
		self.capacityAvailableAB +=bandwidth
		self.capacityAvailableBA +=bandwidth
		assert(0<=self.capacityAvailableAB<=self.totalCapacity)
		assert(0<=self.capacityAvailableBA<=self.totalCapacity)

	def unReserveBWFromDevice(self, _bw, device):
		if device == self.deviceA:
			self.capacityAvailableAB += _bw
			assert(self.capacityAvailableAB <= self.totalCapacity)
		if device == self.deviceB:
			self.capacityAvailableBA += _bw
			assert(self.capacityAvailableBA <= self.totalCapacity)

	def unReserveBW_AB(self, _bw):
		self.capacityAvailableAB += _bw
		assert(self.capacityAvailableAB <= self.totalCapacity)

	def unReserveBW_BA(self, _bw):
		self.capacityAvailableBA += _bw
		assert(self.capacityAvailableBA <= self.totalCapacity)

# Getter functions
	def getAvailableBW(self, device):
		if device == self.deviceA:
			return self.capacityAvailableAB
		if device == self.deviceB:
			return self.capacityAvailableBA

	def getMinAvailableBW(self):
		return min(self.capacityAvailableAB, self.capacityAvailableBA)

	def getDevice_A(self):
		return self.deviceA

	def getDevice_B(self):
		return self.deviceB

	def getOtherDevice(self, _device):
		if self.deviceA == _device:
			return self.deviceB
		if self.deviceB == _device:
			return self.deviceA
	
	def getBothDevices(self):
		return [self.deviceA, self.deviceB]