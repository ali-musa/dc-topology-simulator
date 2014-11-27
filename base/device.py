from component import Component
from enum import *
from vm import VM
import config as cfg
from base.link import Link

class Device(Component):
	def __init__(self, _id, _label, _isHost=False):
		Component.__init__(self, _id, _label)
		self.compType = CompType.DEVICE
		self.isHost = _isHost
		self.VMs = []
		if _isHost:
			self.VMs = [VM(self.id) for x in range(cfg.VMsInHost)]
		self.links = []
	
# over-loaded __str__() for print functionality
	def __str__(self):
		printString = "=========================="
		printString += "\nDevice Information"
		printString += "\n--------------------------"
		printString += "\nID:       " + str(self.id)
		printString += "\nLabel:    " + str(self.label)
		printString += "\nStatus:   " + str(self.status)
		if self.isHost:
			printString += "\nHost device"
		else:
			printString += "\nSwitch device"
		printString += "\n=========================="
		return printString

# Setter functions
	def addLink(self, link):
		assert(isinstance(link, Link))
		self.links.append(link)

	def removeLink(self, link):
		assert(isinstance(link, Link))
		self.links.remove(link)

# Getter functions
	def getAvailableVMs(self):
	# returns list of available VMs in host
		availableVMs = []
		for vm in self.VMs:
			if vm.getStatus() == Status.AVAILABLE:
				availableVMs.append(vm)
		return availableVMs
	
	def getInUseVMs(self):
		# returns list of In_Use VMs in host 
		inUseVMs = []
		for vm in self.VMs:
			if vm.getStatus() == Status.IN_USE:
				inUseVMs.append(vm)
		return inUseVMs

	def getNumPorts(self):
		return len(self.links)

	def getAllLinks(self):
		return self.links

	# this is only for host devices
	def getLink(self):
		return self.links[0]

	#return a list neighbouring device objects
	def getNeighbouringDevices(self):
		neighbours = []
		for link in self.links:
			neighbours.append(link.getOtherDevice(self))
		return neighbours
	
	#return a list neighbours as tuples of (link object, device object)
	def getLinksAndNeighbouringDevices(self):
		linksAndNeighbours = []
		for link in self.links:
			linksAndNeighbours.append((link, link.getOtherDevice(self)))
		return linksAndNeighbours