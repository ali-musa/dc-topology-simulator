import sys, os.path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from base.device import Device
from base.link import Link
from base.enum import *

import random

class Topology:
	def __init__(self, _topologyType):
		self.topologyType = _topologyType
		self.devices = dict()
		self.links = dict()
		self.allocations = []

	def setDevices(self, _devices):
		self.devices = _devices
	def setLinks(self, _links):
		self.links = _links
	def setAllocations(self, _allocate):
		self.allocations.append(_allocate)

	def getDevices(self):
		return self.devices
	def getLinks(self):
		return self.links
	def getAllocations(self):
		return self.allocations
	def getHosts(self):
		hosts = []
		for device in self.devices:
			if device.isHost:
				hosts.append(device)
		return hosts


class Tree(Topology):
	def __init__(self, _topologyType):
		Topology.__init__(self, _topologyType)


class NonTree(Topology):
	def __init__(self, _topologyType):
		Topology.__init__(self, _topologyType)
