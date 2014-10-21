from component import Component
from enum import *
from vm import VM

class Device(Component):
	def __init__(self, _id, _label, _isHost):
		Component.__init__(self, _id, _label)
		self.compType = CompType.DEVICE
		self.isHost = _isHost
		self.VMs = []
		if _isHost:
			self.VMs = [VM for x in range(8)]
		self.links = []

# over-loaded __str__() for print functionality
	def __str__(self):
		printString =  "=========================="
		printString += "\nDevice Information"
		printString += "\n--------------------------"
		printString += "\nID:       " + str(self.id)
		printString += "\nLabel:    " + str(self.label)
		printString += "\nStatus:   " + str(self.status)
		if isHost:
			printString += "\nHost device"
		else:
			printString += "\nSwitch device"
		printString += "\n=========================="
		return printString

# Setter functions
	def addLink(self, link):
		self.links.append(link)

	def removeLink(self, link):
		self.links.remove(link)

# Getter functions
	def getAvailableVMs(self):
		return self.availableVMs

	def getNumPorts(self):
		return len(self.links)

	# this is only for host devices
	def getLink(self):
		return self.links[0]