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
		self.graph = dict() #adjacency list
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
		components = path.getComponents()
		for compNumber in range(len(components)):
			component = components[compNumber]
			if(component.addTrafficID(trafficID)): # this fails if trafficID already present, so we dont double reserve links
				if isinstance(component,Link):
					if(duplex):
						component.reserveBandwidth(bw)
					else:
						component.reserveBWFromDevice(bw,components[compNumber-1]) #it is assumed that for each link both of its devices are given in path
	
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
	# updates self._traffic to reflect the new addition
	def allocate(self,traffic): #TODO: fix conflicts with fattree allocate
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
				
				if(cfg.defaultBackupStrategy is BackupStrategy.LOCAL_ROUTING):
					paths = self.allocateLocalRoutes(traffic)
				
				elif(cfg.defaultBackupStrategy is BackupStrategy.END_TO_END):
					paths = self.__findAndReserveDisjointPaths(traffic.getID(),sourceID,destinationID,cfg.numberOfBackups+1,traffic.getBandwidth())

				elif(cfg.defaultBackupStrategy is BackupStrategy.TOR_TO_TOR): 
					assert(cfg.defaultTopology is not TopologyType.NACRE) #will not work for topologies having multiported hosts
					firstPath = self.findPath(sourceID,destinationID,traffic.getBandwidth())
					if firstPath is not None:
						sourceHost = self.devices[sourceID]
						destinationHost = self.devices[destinationID]
						sourceTor = None
						destinationTor = None
						#find source and destination ToRs
						for device in sourceHost.getNeighbouringDevices():
							if device in firstPath.getComponents():
								sourceTor = device
								break
						for device in destinationHost.getNeighbouringDevices():
							if device in firstPath.getComponents():
								destinationTor = device
								break
						assert(sourceTor is not None)
						assert(destinationTor is not None)

						tor2torPaths = self.__findAndReserveDisjointPaths(traffic.getID(),sourceTor.getID(),destinationTor.getID(),cfg.numberOfBackups+1,traffic.getBandwidth(),cfg.duplexReservation)
						if tor2torPaths:
							#reserve and append once the path from sourceHost to sourceTor and destinationHost to destinationTor
							sourceHost2TorPath = Path([sourceHost,sourceHost.getLinkToDevice(sourceTor), sourceTor])
							destinationTor2HostPath = Path([destinationTor,destinationHost.getLinkToDevice(destinationTor), destinationHost])
							self._reservePath(sourceHost2TorPath,traffic.getBandwidth(),traffic.getID(),cfg.duplexReservation)
							self._reservePath(destinationTor2HostPath,traffic.getBandwidth(),traffic.getID(),cfg.duplexReservation)
							while tor2torPaths:
								completePathComponents = []
								for component in sourceHost2TorPath.getComponents():
									completePathComponents.append(component)
								for component in tor2torPaths[0].getComponents():
									completePathComponents.append(component)
								for component in destinationTor2HostPath.getComponents():
									completePathComponents.append(component)
								paths.append(Path(completePathComponents))
								del tor2torPaths[0]
								gc.collect()
							del sourceHost2TorPath
							del destinationTor2HostPath
							gc.collect()
					self.populateGraph() #TODO: need a more optimized fcn here
				else:
					raise NotImplementedError("Not yet implemented for other backup strategies")

				if paths:
					self._addTraffic(traffic)
					traffic.paths = paths
					traffic.primaryPath = traffic.paths[0] #set the first path as primary
					traffic.inUsePath = traffic.primaryPath #set primary path as the in use path TODO: what if this is failed
					self._setTrafficLocalComponentStatus(traffic,paths) # set initial component statuses
					globals.simulatorLogger.info("Successfully allocated Traffic ID: "+str(traffic.getID()))
					for path in paths:
						globals.metricLogger.debug("Hoplength: %s" % path.getHopLength())

					return True
				else:
					return False
			else:
				raise NotImplementedError("Not implemented for other allocataion schemes yet")
		else:
			raise NotImplementedError("Allocate function has not yet been implemented for other traffic classes")
	
	def deallocate(self,traffic):
		raise NotImplementedError("Yet to implement")

	def allocateLocalRoutes(self, traffic):
		#finds all local routes by failing links along the primary path and then calculating new paths from each point of failure.
		#reserves and returns all these paths
		#TODO: does not deal with device failures
		primaryPath = self.findPath(traffic.sourceID, traffic.destinationID, traffic.getBandwidth())
		if primaryPath is None:
			return []
		paths = [primaryPath]
		devices = (x for x in primaryPath.getComponents() if isinstance(x,Device))
		previousDevice = None
		originalBw = None
		for device in devices:
			if previousDevice:
				originalBw = self.graph[previousDevice.getID()][device.getID()]
				self.updateGraphLinkBw(previousDevice.getID(),device.getID(),0) #set the bandwidth to zero to mark as failed
				localPath = self.findPath(previousDevice.getID(), traffic.destinationID, traffic.getBandwidth())
				if localPath:
					paths.append(localPath)
				self.updateGraphLinkBw(previousDevice.getID(), device.getID(), originalBw) #set the original bandwidth back
			previousDevice = device

		completePaths = [primaryPath]
		for path in paths: # reserve paths
			self._reservePath(path,traffic.getBandwidth(),traffic.getID(),cfg.duplexReservation) #this fcn takes care of overreservation
			#complete the partial paths #TODO: refactor the code below
			if path is not primaryPath:
				completeComps = []
				pathComps = path.getComponents()
				for comp in primaryPath.getComponents():
					if comp in pathComps:
						break
					completeComps.append(comp) 
				completeComps = completeComps+pathComps
				completePaths.append(Path(completeComps))

		self.populateGraph() #update the entire graph TODO: make a more optimized funciton
		return completePaths
		
		

	def __findAndReserveDisjointPaths(self,trafficID,sourceID,destinationID,numberOfPathsToReserve,bandwidth=0, duplex=True):
	#tries to find and reserve disjoint paths given sourceID and destinationID. On success, returns a list of disjoint paths reserved.
	#returns an empty list on failure (also unreserves any misallocated paths)
		paths = []
		for pathNumber in range(numberOfPathsToReserve):
			path = self.findDisjointPath(sourceID,destinationID,bandwidth,paths)
			if path is not None:
				paths.append(path)
				self._reservePath(path,bandwidth,trafficID,duplex)
				
			else: #unable to allocate flow
				#unreserve any allocated paths for this flow
				globals.simulatorLogger.warning("Unable to allocate Traffic ID: "+str(trafficID))
				for path in paths:
					globals.simulatorLogger.debug("Unreserving misallocated paths for Traffic ID: "+str(trafficID))
					self._unreservePath(path,bandwidth,trafficID)
				globals.simulatorLogger.debug("Successfully unreserved any misallocated paths for Traffic ID: "+str(trafficID))
				return []
		return paths

	def _setTrafficLocalComponentStatus(self,traffic,paths):
		#set initial traffic local component status information
		for path in paths:
			for component in path.getComponents():
				componentID = component.getID()
				if componentID not in traffic.localPathComponentStatus:
					traffic.localPathComponentStatus[componentID] = component.getStatus()
	
	def printTopology(self):
		return helper.printTopology(self)
		
	def findPath(self, sourceID, destinationID, bandwidth = 0):
	#takes in sourceID, destinationID and the bandwidth(optional)
	#retuns the first shortest path with atleast the BW specified as an object of Path class, if such a path is found else returns None
		pathDevIDs = self.shortest_path(sourceID,destinationID,bandwidth)
		if pathDevIDs:
			path = []
			for id in pathDevIDs:
				if path:
					path.append(path[-1].getLinkToDevice(self.devices[id]))
				path.append(self.devices[id])
			return Path(path)
		return None
		#return self.findDisjointPath(sourceID,destinationID,bandwidth)

	def findDisjointPath(self, sourceID, destinationID, bandwidth = 0, existingPaths=[]):
	#takes in sourceID, destinationID, bandwidth(optional) and a list of paths
	#retuns the first shortest disjoint path with atleast the BW specified as an object of Path class, if such a path is found else returns None
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
		self.populateGraph()
########### NEW CODE END

########### New bfs code ref: http://eddmann.com/posts/depth-first-search-and-breadth-first-search-in-python/
	def populateGraph(self):
		for dev in self.devices.keys():
			neighbours = dict()
			for neighbour in self.devices[dev].getNeighbouringDevices():
				neighbours[neighbour.getID()]= self.devices[dev].getLinkToDevice(neighbour).getAvailableBWFromDevice(self.devices[dev])
			self.graph[dev] = neighbours

	def updateGraphLinkBw(self, fromDeviceID, toDeviceID, newBw): #TODO: use this function at every failure, recovery, allocation and recovery
		self.graph[fromDeviceID][toDeviceID] = newBw

	def bfs_paths(self, start, goal, bw = 0):
		queue = [(start, [start])]
		while queue:
			(vertex, path) = queue.pop(0)
			remainingPath = (x for x in self.graph[vertex].keys() if x not in path)
			for next in	remainingPath:
				if self.graph[vertex][next]<bw:
					continue
				if next == goal:
					yield path + [next]
				else:
					queue.append((next, path + [next]))

		
	def bfs_paths_optimized(self, start, goal, bw = 0): #might not work for all shortest paths or all paths (use unoptimized one)
		queue = [(start, [start])]
		verticesSeen = []
		while queue:
			(vertex, path) = queue.pop(0)
			if vertex in verticesSeen:
				continue
			verticesSeen.append(vertex)
			remainingPath = (x for x in self.graph[vertex].keys() if x not in path)
			for next in	remainingPath:
				if self.graph[vertex][next]<bw:
					continue
				if next == goal:
					yield path + [next]
				else:
					queue.append((next, path + [next]))

	def shortest_path(self, start, goal, bw = 0):
		try:
			return next(self.bfs_paths_optimized(start, goal, bw))
		except StopIteration:
			return None

	def shortest_paths(self, start, goal, bw = 0):
		allPaths = self.bfs_paths(start, goal, bw)
		paths = []
		try:
			paths.append(next(allPaths))
			shortestLength = len(paths[0])
			while(True):
				try: 
					nextPath = next(allPaths)
					if(len(nextPath)> shortestLength):
						return paths
					paths.append(nextPath)
				
				except StopIteration:
					return paths
							
		except StopIteration:
			return paths


class Tree(Topology):
	def __init__(self, _topologyType):
		Topology.__init__(self, _topologyType)


class NonTree(Topology):
	def __init__(self, _topologyType):
		Topology.__init__(self, _topologyType)

class Custom(Topology):
	#TODO: implement custom here
	pass

