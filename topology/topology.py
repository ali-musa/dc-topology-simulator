import sys, os.path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from base.device import Device
from base.link import Link
from base.enum import *
from base.queue import Queue

import random
import csv

# to-do: this function should go in a util class/file
def findValue(line, param):
	i = 0
	for l in line:
		if l == param:
			return line[i+1]
		i+=1
	return None

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

########### NEW CODE BELOW

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

	def generate(self):
		fname = raw_input("Enter filename to load topology from: ")
		lines = []
		with open(fname,'rb') as fin:
			reader = csv.reader(fin,delimiter=' ')
			for row in reader:
				lines.append(row)

		linkID_default = 0 # incrementally used if no linkIDs are given from file
		for line in lines:
			header = line[0]
			if header == "#connect":
				# compulsory parameters
				deviceA_id = findValue(line, "-deviceA")
				deviceB_id = findValue(line, "-deviceB")
				typeA_val = findValue(line, "-typeA")
				typeB_val = findValue(line, "-typeB")
				typeA = False
				typeB = False

				if typeA_val == "host":
					typeA = True

				if typeB_val == "host":
					typeB = True

				# optional parameters
				labelA = findValue(line, "-labelA")
				labelB = findValue(line, "-labelB")
				bw = findValue(line, "-bw")
				linkLabel = findValue(line, "-linkLabel")
				linkID = findValue(line, "-linkID")

				if linkLabel is None:
					linkLabel = "link"

				if linkID is None:
					linkID = linkID_default
					linkID_default+=1
				
				if bw is None:
					bw = 0
				
				if labelA is None:
					labelA = "device"

				if labelB is None:
					labelB = "device"
				
				deviceA = None
				deviceB = None

				# if device already exists, use that. else make a new one.
				if self.devices.has_key(deviceA_id):
					deviceA = self.devices[deviceA_id]
				else:
					deviceA = Device(deviceA_id, labelA, typeA)	
				
				if self.devices.has_key(deviceB_id):
					deviceB = self.devices[deviceB_id]
				else:
					deviceB = Device(deviceB_id, labelB, typeB)	
				
				link = Link(linkID, linkLabel, bw, deviceA, deviceB)
				
				# add link and devices to topology
				self.devices[deviceA_id] = deviceA
				self.devices[deviceB_id] = deviceB
				self.links[linkID] = link

				# connect the devices
				deviceA.addLink(link)
				deviceB.addLink(link)

########### NEW CODE END
				
class Tree(Topology):
	def __init__(self, _topologyType):
		Topology.__init__(self, _topologyType)


class NonTree(Topology):
	def __init__(self, _topologyType):
		Topology.__init__(self, _topologyType)

class Custom(Topology):
    #TODO: implement custom here
    pass

