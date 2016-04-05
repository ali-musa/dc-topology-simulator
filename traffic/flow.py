import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from traffic import Traffic
from base.enum import *
from base.path import Path
import config as cfg
import globals as globals
#from base.event import *

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
		if(BackupStrategy.FLEXIBLE_REPLICA==cfg.defaultBackupStrategy or BackupStrategy.LOCAL_ROUTING==cfg.defaultBackupStrategy):
			return 0
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
		if(BackupStrategy.FLEXIBLE_REPLICA==cfg.defaultBackupStrategy or BackupStrategy.LOCAL_ROUTING==cfg.defaultBackupStrategy):
			return
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
	def isHigherPriorityPathAvailableToBackup(self, inUsePath):
		#check locally if a higher priority backup path is available and returns true, else false
		currentPri = inUsePath.getPriority()
		for path in self.paths:
			if((path.getPriority()>currentPri) and (not self.isFailedLocal(path))):#check if any higher priority path is up locally
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
		#assert(self.inUsePath is None) #ideally should not backup as long as there is already a path in use
		if(self.inUsePath is None):
			for path in self.paths:
				if(not self.isFailedLocal(path)): #backup to any path that is not failed #TODO: check for capacity along the backup in the backup sharing scheme
					self.inUsePath = path
					break
		if(self.inUsePath is None):
			return
		#at this point the inUsePath will be up (if it was not None originally then it must be up aswell)
		for path in self.paths:
			if((path.getPriority()>self.inUsePath.getPriority()) and (not self.isFailedLocal(path))):
				self.inUsePath = path

	def reactToFailure(self,failureTime,failedCompID):
		if (self.inUsePath is not None):
			if((self.downFromTime == None) and (self.inUsePath.isFailed())):
				#if the flow was getting service and failure is on the path that was in use
				self.addInFlightDataTimePenalty(failedCompID)
				self.downFromTime = failureTime
			else:
				#either the failure is not on the path being used, or the flow was already not getting any service
				pass
		else:
			#the flow is paused
			pass
		return [EventType.FAILURE_MSG, failureTime + float(self.getDetectionTime(failedCompID))]

	def reactToRecovery(self,recoveryTime,recoveredCompID):
		if(self.downFromTime!=None): #not getting service
			if(self.inUsePath!=None):
				if(not self.inUsePath.isFailed()):
					self.addDowntime(recoveryTime-self.downFromTime)
					self.downFromTime = None
				else:
					#recovery did not bring the traffic up
					pass
			else:
				#traffic is paused, any recovery cannot bring it service
				pass
		else:
			#traffic is getting service already, any recovery will keep the same state
			pass
		return [EventType.RECOVERY_MSG, recoveryTime+float(self.getDetectionTime(recoveredCompID))]

	def reactToFailureMsg(self, failureMsgTime, failedCompID):
		evInfo = None
		#update local component status
		self.localPathComponentStatus[failedCompID] = Status.FAIL
		if (self.inUsePath is not None):
			if(self.isFailedLocal(self.inUsePath)):
				#in use path failed
				if(self.isBackupPossible()): #based on local knowledge
					evInfo = [EventType.BACKUP, failureMsgTime+self.getReactionTime()]
				else:
					#backup not possible
					pass
				# pause flow
				self.inUsePath = None
				if(self.downFromTime==None):
					#start downtime
					self.downFromTime = failureMsgTime
				else:
					#was already not getting service, downtime already started
					pass

			else:
				#failure is not on the in use path
				pass
		else:
			#Flow paused failure message will not do anything
			pass
		return evInfo

	def reactToRecoveryMsg(self, recoveryMsgTime, recoveredCompID):
		evInfo = None
		#update local component status
		self.localPathComponentStatus[recoveredCompID] = Status.AVAILABLE
		if(self.inUsePath == None):
			if(self.isBackupPossible()): #based on local knowledge
				evInfo = [EventType.BACKUP, recoveryMsgTime+self.getReactionTime()]
			else:
				#backup not possible
				pass
		else:
			if(self.isHigherPriorityPathAvailableToBackup(self.inUsePath)): #flow is un-paused but not on the heighest pri path
				evInfo = [EventType.BACKUP, recoveryMsgTime+self.getReactionTime()]
			else:
				#flow is un-paused and already on the highest priority available path, recovery message will not do anything
				pass
		return evInfo

	def reactToBackup(self, backupTime):
		#attempt backup
		self.backup()
		if(self.inUsePath is not None):
			#backup successful locally or continuing on the old inUsePath
			if(self.downFromTime is not None):
				#was down globally
				if(not self.inUsePath.isFailed()):#check if the backup was successful gloablly
					#backup successful globally as well
					self.addDowntime(backupTime - self.downFromTime)
					self.downFromTime = None
				else:
					#backup unsuccessful globally, already not getting service so pass
					pass
			else:
				#was initially up globally
				if(not self.inUsePath.isFailed()):#check if the backup to higher pri was successful gloablly
					#backup successful globally as well
					pass
				else:
					#backup to higher pri forced it into downtime
					self.downFromTime = backupTime

		else:
			#backup unsuccessful
			pass

		return None
