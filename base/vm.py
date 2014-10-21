from enum import *

class VM:
	def __init__(self):
		self.status = Status.AVAILABLE;
		self.traffic_id = 0;

# over-loaded __str__() for print functionality
	def __str__(self):
		printString =  "=========================="
		printString += "\nVM Information"
		printString += "\n--------------------------"
		printString += "\nStatus:      " + str(self.status)
		printString += "\nTraffic ID:  " + str(self.traffic_id)
		printString += "\n=========================="
		return printString

# Setter functions
	def setID(self, _id):
		self.traffic_id = _id

	def setStatus(self, _status):
		self.status = _status

# Getter functions
	def getID(self):
		return self.traffic_id

	def getStatus(self):
		return self.status
