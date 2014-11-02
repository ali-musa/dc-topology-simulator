import sys, os.path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from base.device import Device
from base.link import Link
from base.enum import *
from base.queue import Queue

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

	def printTopo(self):				# breadth first search of the entire topology
		print "Starting BFS..."
		print

		start = self.devices[self.devices.keys()[0]] # start from the first device
		start.setDistance(0)
		start.setPredecessor(None)
		vertQueue = Queue()
		vertQueue.enqueue(start)
		while(vertQueue.size() > 0):
			currentVert = vertQueue.dequeue()
			for nbr in currentVert.getNeighbours():
				if nbr.getColor() == "white":		# the node is not yet visited
					nbr.setColor("gray")			# marks the node as currently being processed
					nbr.setDistance(currentVert.getDistance() + 1)
					nbr.setPredecessor(currentVert)
					vertQueue.enqueue(nbr)
			currentVert.setColor("black")			# the node has been visited
			print currentVert
		self.reset()
		
		print
		print "Finished BFS on entire topology!"
		return


	def reset(self):					# reset the path-finding details on all nodes
		for _id, _device in self.devices.iteritems():
			_device.setDistance(0)
			_device.setPredecessor(None)
			_device.setColor("white")


	def findPath(self, _start, _end):		# breadth first seach starting at "start" node

		start = self.devices[_start] # start node
		end = self.devices[_end] # end node

		print "Finding path from %s to %s" % (start.id, end.id)
		print
		
		start.setDistance(0)
		start.setPredecessor(None)
		vertQueue = Queue()
		vertQueue.enqueue(start)
		while(vertQueue.size() > 0):
			currentVert = vertQueue.dequeue()
			print currentVert

			if currentVert.id == end.id:
				currentVert.setColor("black")
				path = []
				while currentVert.getPredecessor() != None:
					path.append(currentVert.getPredecessor())
					currentVert = currentVert.getPredecessor()
				self.reset()
				print len(path)
				return path

			for nbr in currentVert.getNeighbours():
				if nbr.getColor() == "white":		# the node is not yet visited
					nbr.setColor("gray")			# marks the node as currently being processed
					nbr.setDistance(currentVert.getDistance() + 1)
					nbr.setPredecessor(currentVert)
					vertQueue.enqueue(nbr)
			currentVert.setColor("black")			# the node has been visited


class Tree(Topology):
	def __init__(self, _topologyType):
		Topology.__init__(self, _topologyType)


class NonTree(Topology):
	def __init__(self, _topologyType):
		Topology.__init__(self, _topologyType)
