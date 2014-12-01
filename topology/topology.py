import sys
import os.path
from __builtin__ import isinstance
from exceptions import NotImplementedError
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from base.device import Device
from base.link import Link
from base.enum import *
from base.path import Path

import config as cfg
import globals as globals
from traffic.traffic import *
from traffic.flow import *
from traffic.tenant import *
from utils.helper import *


import random
import csv

class Topology:
	def __init__(self, _topologyType):
		self.topologyType = _topologyType
		self.devices = dict()
		self.links = dict()
	#protected members
		self._traffics = dict() 

	#protected methods
	def _addTraffic(self, traffic):
		assert(traffic not in self._traffics.values())
		self._traffics[traffic.getID()] = traffic

	def _removeTraffic(self, traffic):
		assert(traffic in self._traffics.values())
		del self._traffics[traffic.getID()]
		gc.collect() #force garbage collection
	
	def _reservePath(self,path, bw, trafficID,duplex=True):
		assert path
		for component in path.getComponents():
			component.addTrafficID(trafficID)
			if isinstance(component,Link):
				if(duplex):
					component.reserveBandwidth(bw)
				else:
					raise NotImplementedError("Uni directional path reservation has not been implemented")
	
	def _unreservePath(self,path, bw, trafficID,duplex=True): 
		assert path
		for component in path.getComponents():
			component.removeTrafficID(trafficID)
			if isinstance(component,Link):
				if(duplex):
					component.unReserveBandwidth(bw)
				else:
					raise NotImplementedError("Uni directional path reservation has not been implemented")
			
###############################
	#public methods
	def getAllTraffic(self):
		return self._traffics
	def getTrafficsUsingComponentID(self, componentID):
		traffics = []
		if componentID in self.devices:
			for trafficID in self.devices[componentID].getTrafficIDs():
				traffics.append(self._traffics[trafficID])
		if componentID in self.links:
			for trafficID in self.links[componentID].getTrafficIDs():
				traffics.append(self._traffics[trafficID])
		return traffics
		
	def getDevices(self):
		return self.devices
	def getLinks(self):
		return self.links
	def getHosts(self):
		hosts = dict()
		for deviceId, device in self.devices.iteritems():
			if device.isHost:
				hosts[deviceId] = device
		return hosts
	
	def connectDeviceAB(self,deviceA,deviceB,linkLabel=None):
		link = Link(str(deviceA.getID()) + "_" + str(deviceB.getID()),linkLabel,cfg.bandwidthPerLink,deviceA,deviceB)
		self.links[link.getID()] = link
		deviceA.addLink(link)
		deviceB.addLink(link)
		return True

	def createDevice(self,deviceId,label, isHost=False):
		device = Device(deviceId,label,isHost)
		self.devices[deviceId] = device
		return device
		
	def failComponentByID(self, compID):
		try:
			comp = self.devices[compID]
		except:
			comp = self.links[compID]
		comp.setStatus(Status.FAIL)

	def recoverComponentByID(self, compID):
		try:
			comp = self.devices[compID]
		except:
			comp = self.links[compID]
		comp.setStatus(Status.AVAILABLE)
	
	# takes in an instance of a Traffic subclass, returns true if allocate is successful
	# inserts primary and backup information in the passed instance
	# updates the self._traffic to reflect the new addition
	def allocate(self,traffic): 
		assert isinstance(traffic,Traffic)
		globals.simulatorLogger.info("Allocating Traffic ID: "+str(traffic.getID()))
		if isinstance(traffic,Flow):
			if(AllocationStrategy.RANDOM_SOURCE_DESTINATION == cfg.defaultAllocationStrategy):
				#choose random source destination pair
				sourceID = random.choice(self.getHosts().keys())
				destinationID = random.choice(self.getHosts().keys())
				while sourceID == destinationID:
					destinationID = random.choice(self.getHosts().keys())
				traffic.sourceID = sourceID
				traffic.destinationID = destinationID
				paths=[]
				for backupNumber in range(cfg.numberOfBackups+1):
					path = self.findDisjointPath(traffic.sourceID, traffic.destinationID,traffic.getBandwidth(),paths)
					if path:
						paths.append(path)
						self._reservePath(path,traffic.getBandwidth(),traffic.getID())
						#set traffic local component status information
						for component in path.getComponents():
							componentID = component.getID()
							if componentID not in traffic.localPathComponentStatus:
								traffic.localPathComponentStatus[componentID] = component.getStatus()
					else: #unable to allocate flow
						#unreserve any allocated paths for this flow
						globals.simulatorLogger.warning("Unable to allocate Traffic ID: "+str(traffic.getID()))
						traffic.localPathComponentStatus.clear()
						for path in paths:
							globals.simulatorLogger.debug("Unreserving misallocated paths for Traffic ID: "+str(traffic.getID()))
							self._unreservePath(path,traffic.getBandwidth(),traffic.getID())
						globals.simulatorLogger.debug("Successfully unreserved any misallocated paths for Traffic ID: "+str(traffic.getID()))
						return False
				self._addTraffic(traffic)
				traffic.paths = paths
				traffic.primaryPath = traffic.paths[0] #set the first path as primary
				traffic.inUsePath = traffic.primaryPath #set primary path as the in use path
				globals.simulatorLogger.info("Successfully allocated Traffic ID: "+str(traffic.getID()))
				return True
			else:
				raise NotImplementedError("Not implemented for other allocataion schemes yet")
		else:
			raise NotImplementedError("Allocate function has not yet been implemented for other traffic classes")
	
	def deallocate(self,traffic):
		raise NotImplementedError("Yet to implement")


	def printTopology(self):
		return helper.printTopology(self)
		
	#takes in sourceID, destinationID and the bandwidth(optional)
	#retuns the first shortest path with atleast the BW specified as an object of Path class, if such a path is found else returns None
	def findPath(self, sourceID, destinationID, bandwidth = 0):
		return self.findDisjointPath(sourceID,destinationID,bandwidth)
	#takes in sourceID, destinationID, bandwidth(optional) and a list of paths
	#retuns the first shortest disjoint path with atleast the BW specified as an object of Path class, if such a path is found else returns None
	def findDisjointPath(self, sourceID, destinationID, bandwidth = 0, existingPaths=[]):
		return helper.findDisjointPathBFS(self, self.devices[sourceID],self.devices[destinationID],  bandwidth, existingPaths)

	
########### TODO: Refactor the code below

	def generate(self):
		fname = cfg.customTopoFilename
		if(cfg.overrideDefaults):
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
				deviceA_id = helper.findValue(line, "-deviceA")
				deviceB_id = helper.findValue(line, "-deviceB")
				typeA_val = helper.findValue(line, "-typeA")
				typeB_val = helper.findValue(line, "-typeB")
				typeA = False
				typeB = False

				if typeA_val == "host":
					typeA = True

				if typeB_val == "host":
					typeB = True

				# optional parameters
				labelA = helper.findValue(line, "-labelA")
				labelB = helper.findValue(line, "-labelB")
				bw = helper.findValue(line, "-bw")
				linkLabel = helper.findValue(line, "-linkLabel")
				linkID = helper.findValue(line, "-linkID")

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

				# if device already exists, use that.  else make a new one.
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

