import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from traffic import Traffic
from base.enum import TrafficPriority
from base.path import Path
import config as cfg
import globals as globals

class Flow(Traffic):
	def __init__(self, startTime, duration, sourceID, destinationID, bandwidth, priority=TrafficPriority.NORMAL):
		Traffic.__init__(self, startTime, duration, priority)
		
		#private members
		self.__sourceID = sourceID
		self.__destinationID = destinationID
		self.__bandwidth = bandwidth
		
		#public members
		self.paths = []
		self.primaryPath = None
		self.inUsePath = None
		
	#public methods
	#def getID(self):
	#	return super(Flow, self).getID()
	#def getEndTime(self):
	#	return super(Flow, self).getEndTime()
	def __str__(self):
		printString = super(Flow,self).__str__()
		printString +='\nSourceID:		  ' + str(self.__sourceID)
		printString +='\nDestinationID:	  ' + str(self.__destinationID)
		printString +='\nBandwidth: 	  ' + str(self__.bandwidth)
	
		if self.paths:
			printString +='\nNumber of paths: ' + str(len(self.paths))
		if self.primaryPath is not None:
			printString +='\nPrimary path ID: ' + str(self.primaryPath.getID())
		if self.inUsePath is not None:
			printString +='\nPath in use ID:  ' + str(self.inUsePath.getID())
		return printString
	def getSourceID(self):
		return self.__sourceID
	def getDestinationID(self):
		return self.__destinationID
	def getBandwidth(self):
		return self.__bandwidth
	#def addPath(self, path):
	#	assert(path not in paths)
	#	self.paths.append(path)
	
	#def getPaths(self):
	#	return self.paths

	#def setInUsePath(self, path):
	#	#set traffic id in each component
	#	self.inUsePath = path

	#def getInUsePath(self):
	#	return self.inUsePath

	#def setPrimaryPath(self, path, bandwidth):
	#	self.primaryPath = path
	
	#def getPrimaryPath(self, path):
	#	return self.primaryPath

	def switchToBackup():
		raise NotImplementedError

	def revertToPrimary():
		raise NotImplementedError
	
	def initialize(self):
		#TODO: set traffic id in topology (dont do this here though)
		if(globals.topologyInstance.allocate(self)):
			globals.metricLogger.info('FlowID: %s allocated' % self.getID())
			return True
		else:
			return False


	