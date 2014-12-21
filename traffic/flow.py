import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from traffic import Traffic
from base.enum import TrafficPriority
from base.enum import Status
from base.path import Path
import config as cfg
import globals as globals

class Flow(Traffic):
	def __init__(self, startTime, duration, bandwidth, priority=TrafficPriority.NORMAL):
		Traffic.__init__(self, startTime, duration, priority)
		
		#private members
		self.__bandwidth = bandwidth #in Megabits
		self.__downtime = 0.0
		
		#public members (these will be set when the flow is allocated in the topology)
		self.sourceID = None
		self.destinationID = None
		self.paths = []
		self.primaryPath = None
		self.inUsePath = None
		self.localPathComponentStatus = dict()
		self.downFromTime = None #this variable should be none when the flow is getting service
		
	#public methods
	def __str__(self):
		printString = super(Flow,self).__str__()
		printString +='\nBandwidth: 	  ' + str(self.__bandwidth)
		if self.sourceID is not None:
			printString +='\nSourceID:		  ' + str(self.sourceID)
		if self.destinationID is not None:
			printString +='\nDestinationID:	  ' + str(self.destinationID)
		if self.paths:
			printString +='\nNumber of paths: ' + str(len(self.paths))
		if self.primaryPath is not None:
			printString +='\nPrimary path ID: ' + str(self.primaryPath)
		if self.inUsePath is not None:
			printString +='\nPath in use ID:  ' + str(self.inUsePath)
		printString +='\nDowntime:  	  ' + str(self.__downtime)
		return printString
	
	def getBandwidth(self):
		return self.__bandwidth
	
	def initialize(self):
		if(globals.topologyInstance.allocate(self)):
			globals.simulatorLogger.info('FlowID: %s allocated' % self.getID())
			return True
		else:
			return False

	def unInitialize(self):
		raise NotImplementedError
	
	def getDetectionTime(self, failedComponentID):
		return (self.__getHoplengthFromSourceByComponentID(failedComponentID)*cfg.messageDelayPerHop)

	def __getHoplengthFromSourceByComponentID(self,componentID):
		for path in self.paths:
			hoplength = 0
			for component in path.getComponents():
				#asssuming that the first item in the path components list is always the source
				if(component.getID() == componentID):
					return hoplength
				hoplength+=1
		assert(False) #the componentID supplied was not found in the paths list

	def getReactionTime(self):
		return cfg.backupReactionTime
	
	def addInFlightDataTimePenalty(self, failedComponentID):
		self.__downtime += (self.__getHoplengthFromSourceByComponentID(failedComponentID)*cfg.dataDelayPerHop)

	def addDowntime(self, downtime):
		assert(downtime>=0)
		self.__downtime+=downtime

	def getDowntime(self, currTime):
		
		if (self.downFromTime is None):
			return self.__downtime
		else:
			assert(self.downFromTime<=currTime) #current time should be after downFromTime
			return self.__downtime + (currTime-self.downFromTime)

	def isBackupPossible(self):
		#checks locally if backup is possible and returns true else false
		for path in self.paths:
			if(not self.isFailedLocal(path)): #check if any path is up locally
				return True
		return False
	
	def isFailedLocal(self, path):
		#Analagous to isFailed path class function
		#Takes a path object as input and checks locally if the path is failed and return True, else false
		for component in path.getComponents():
			if self.localPathComponentStatus[component.getID()] == Status.FAIL:
				return True
		return False

	def backup(self):
		#attempt backup on local knowledge and set inUse path accordingly
		assert(self.inUsePath is None) #ideally should not backup as long as there is already a path in use
		for path in self.paths:
			if(not self.isFailedLocal(path)): #backup to any path that is not failed #TODO: check for capacity along the backup in the backup sharing scheme
				self.inUsePath = path
				return