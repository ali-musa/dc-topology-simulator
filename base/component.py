from enum import *

class Component:
	def __init__(self, _id, _label):
		self.id = _id
		self.label = _label
		self.status = Status.AVAILABLE
		self.compType = None
		self.trafficID = []

# Setter functions
	def setStatus(self, _status):
		self.status = _status

# Getter functions
	def getID(self):
		return self.id;

	def getLabel(self):
		return self.label

	def getStatus(self):
		return self.status

	def getType(self):
		return self.compType
