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
from reservation.traffic import *
from reservation.flow import *
from reservation.tenant import *
from utils.helper import *


import random
import csv

class Topology:
	def __init__(self, _topologyType):
		self.topologyType = _topologyType
		self.devices = dict()
		self.links = dict()
	#protected members
		self._traffic = dict() #TODO: fix the functions associated with _trafficIDs

	#def setDevices(self, _devices):
	#	self.devices = _devices
	#def setLinks(self, _links):
	#	self.links = _links
	
	#private methods
	def addTraffic(self, _traffic): #TODO: refactor this function
		self._traffic[_traffic.getID()] = _traffic

	def __addTrafficID(self, _trafficID):
		assert(_trafficID not in self._trafficIDs)
		self._trafficIDs.append(_trafficID)
	
	def __removeTrafficID(self, _trafficID):
		assert(_trafficID in self._trafficIDs)
		self._trafficIDs.remove(_trafficID)
	
	def __reservePath(self,path, bw, trafficID,duplex=True): #private function
		assert path
		for component in path.getComponents():
			component.addTrafficID(trafficID)
			if isinstance(component,Link):
				if(duplex):
					component.reserveBW(bw)
				else:
					raise NotImplementedError("Uni directional path reservation has not been implemented")
	
	def __unreservePath(self,path, bw, trafficID,duplex=True): #private function
		assert path
		for component in path.getComponents():
			component.removeTrafficID(trafficID)
			if isinstance(component,Link):
				if(duplex):
					component.unreserveBW(bw)
				else:
					raise NotImplementedError("Uni directional path reservation has not been implemented")
			
###############################
	#public methods
	def getTrafficIDs(self):
		return self._trafficIDs

	def getDevices(self):
		return self.devices
	def getLinks(self):
		return self.links
	def getAllocations(self):
		return self._trafficIDs
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
		
	def failComponentById(self, compID):
		try:
			comp = self.devices[compID]
		except:
			comp = self.links[compID]
		comp.setStatus(Status.FAIL)

	def recoverComponentById(self, compID):
		try:
			comp = self.devices[compID]
		except:
			comp = self.links[compID]
		comp.setStatus(Status.AVAILABLE)
	
	# takes in an instance of a Traffic subclass, returns true if allocate is successful
	# inserts primary and backup information in the passed instance
	# updates the self.TrafficIDs to reflect the new addition
	def allocate(self,traffic): 
		assert isinstance(traffic,Traffic)
		globals.simulatorLogger.info("Allocating Traffic ID: "+str(traffic.getID()))
		if isinstance(traffic,Flow):
			paths=[]
			for backupNumber in range(cfg.numberOfBackups):
				path = self.findPath(traffic.getSourceID(), traffic.getDestinationID(),traffic.getBandwidth())
				#TODO: make and use findDisjointPath function
				if path:
					paths.append(path)
					self.__reservePath(path,traffic.getBandwidth(),traffic.getID())

				else: #unable to allocate flow
					#unreserve any allocated paths for this flow
					globals.simulatorLogger.warning("Unable to allocate Traffic ID: "+str(traffic.getID()))
					for path in paths:
						globals.simulatorLogger.debug("Unreserving misallocated paths for Traffic ID: "+str(traffic.getID()))
						self.__unreservePath(path,traffic.getBandwidth(),traffic.getID())
					globals.simulatorLogger.debug("Successfully unreserved any misallocated paths for Traffic ID: "+str(traffic.getID()))
					return False
			self.__addTrafficID(traffic.getID())
			traffic.paths = paths
			traffic.primaryPath = traffic.paths[0] #set the first path as primary
			traffic.inUsePath = traffic.primaryPath #set primary path as the in use path
			globals.simulatorLogger.info("Successfully allocated Traffic ID: "+str(traffic.getID()))
			return True
		else:
			raise NotImplementedError("Allocate function has not yet been implemented for other traffic classes")
	
	def deallocate(self,traffic):
		raise NotImplementedError("Yet to implement")


	def printTopology(self):
		return helper.printTopology(self)
		
	#takes in sourceID, destinationID and the bandwidth(optional)
	#retuns the first shortest path with atleast the BW specified as an object of Path class, if such a path is found else returns None
	def findPath(self, sourceID, destinationID, bandwidth = 0):
		return helper.findShortestPathBFS(self.devices[sourceID],self.devices[destinationID], bandwidth)
	
	
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

