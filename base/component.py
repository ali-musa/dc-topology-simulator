from enum import *

class Component:
	def __init__(self, _id, _label):
		self.id = _id
		self.label = _label
		self.status = Status.AVAILABLE
		self.compType = None
		self.trafficIDs = []

# Setter functions
	def setStatus(self, _status):
		self.status = _status

	def addTrafficID(self, _trafficID):
		if(_trafficID not in self.trafficIDs): #do not add duplicates
			self.trafficIDs.append(_trafficID)
	def removeTrafficID(self, _trafficID):
		if(_trafficID in self.trafficIDs): #do not add duplicates
			self.trafficIDs.remove(_trafficID)

# Getter functions
	def getID(self):
		return self.id

	def getLabel(self):
		return self.label

	def getStatus(self):
		return self.status

	def getType(self):
		return self.compType
