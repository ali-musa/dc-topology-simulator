from failure.failure import *
from enum import *
import uuid
from traffic.tenant import *
from base.path import *
import logging
import globals as globals
from traffic import *
from traffic.flow import *
from traffic.tenant import *
from traffic.traffic import *
from traffic.characteristics import *
from exceptions import NotImplementedError
from base.enum import Status
from utils.helper import *

"""
eventType = "Failure" or "Recovery" or "Arrival" or "Departure" or "End"
"""

class Event:
	def __init__(self, _time, _eventType):
		self.__id = uuid.uuid4()
		self.__time = _time
		self.eventType = _eventType

	def getEventID(self): #TODO: refactor these functions as getID, getTime, getType
		return self.__id
	def getEventTime(self):
		return self.__time
	def getEventType(self):
		return self.eventType

# over-loaded __str__() for print functionality
	def __str__(self):
		printString = "=========================="
		printString += "\nEvent Information"
		printString += "\n--------------------------"
		printString += "\nEvent ID: " + str(self.__id)
		printString += "\nEvent Time: " + str(self.__time)
		printString += "\nEvent Type: " + str(self.eventType)
		printString += "\n=========================="
		return printString

class FailureEvent(Event):
	def __init__(self, _time, _eventType, _objectID):
		Event.__init__(self, _time, _eventType)
		self.compID = _objectID

	def handle(self):
		events = []
		globals.topologyInstance.failComponentByID(self.compID)
		ttR = globals.failureModelInstance.getTTR(self.compID)
		if ttR==-1:
			return []
		recoveryTime = self.getEventTime() + ttR
		events.append(RecoveryEvent(recoveryTime, EventType.RECOVERY, self.compID))

		for traffic in globals.topologyInstance.getTrafficsUsingComponentID(self.compID):
			events.append(FailureMsgEvent(self.getEventTime() + float(traffic.getDetectionTime(self.compID)), traffic))
			if(isinstance(traffic,Flow)):
				if (traffic.inUsePath is not None):
					if((traffic.downFromTime == None) and (traffic.inUsePath.isFailed())):
						#if the flow was getting service and failure is on the path that was in use
						traffic.addInFlightDataTimePenalty(self.compID)
						traffic.downFromTime = self.getEventTime()
					else:
						#either the failure is not on the path being used, or the flow was already not getting any service
						pass
				else:
					#the flow is paused
					pass
			else:
				raise NotImplementedError("Not implemented for other traffic classes yet")

		return events

class RecoveryEvent(Event):
	def __init__(self,_time, _eventType, _objectID):
		Event.__init__(self, _time, _eventType)
		self.compID = _objectID

	def handle(self):
		events = []
		globals.topologyInstance.recoverComponentByID(self.compID)
		ttF = globals.failureModelInstance.getTTF(self.compID)
		if ttF==-1:
			return []
		failureTime = self.getEventTime() + ttF
		events.append(FailureEvent(failureTime, EventType.FAILURE, self.compID))

		for traffic in globals.topologyInstance.getTrafficsUsingComponentID(self.compID):
			events.append(RecoveryMsgEvent(self.getEventTime()+float(traffic.getDetectionTime(self.compID)),traffic))
			if(isinstance(traffic,Flow)):
				if(traffic.downFromTime!=None): #not getting service
					if(traffic.inUsePath!=None):
						if(not traffic.inUsePath.isFailed()):
							traffic.addDowntime(self.getEventTime()-traffic.downFromTime)
							traffic.downFromTime = None
						else:
							#recovery did not bring the traffic up
							pass
					else:
						#traffic is paused, any recovery cannot bring it service
						pass
				else:
					#traffic is getting service already, any recovery will keep the same state
					pass
			else:
				raise NotImplementedError("Not implemented for other traffic classes yet")
		
		return events

class FailureMsgEvent(Event):
	def __init__(self,eventTime, traffic, eventType = EventType.FAILURE_MSG):
		Event.__init__(self,eventTime, eventType)
		self.__traffic = traffic
	
	def handle(self):
		events = []
		if(isinstance(self.__traffic,Flow)):
			#update local component status
			self.__traffic.localPathComponentStatus[self.__traffic.getID] = Status.FAIL
			if (self.__traffic.inUsePath is not None):
				if(self.__traffic.isFailedLocal(self.__traffic.inUsePath)):
					#in use path failed
					if(self.__traffic.isBackupPossible()): #based on local knowledge
						events.append(BackupEvent(self.getEventTime()+self.__traffic.getReactionTime(), traffic))
					else:
						#backup not possible
						pass
					# pause flow
					self.__traffic.inUsePath = None
					if(self.__traffic.downFromTime==None):
						#start downtime
						self.__traffic.downFromTime = self.getEventTime()
					else:
						#was already not getting service, downtime already started
						pass

				else:
					#failure is not on the in use path
					pass
			else:
				#Flow paused failure message will not do anything
				pass
		else:
			raise NotImplementedError("Not implemented for other traffic classes yet")

		return events

class RecoveryMsgEvent(Event):
	def __init__(self,eventTime, traffic, eventType = EventType.RECOVERY_MSG):
		Event.__init__(self,eventTime, eventType)
		self.__traffic = traffic
	
	def handle(self):
		events = []
		if(isinstance(self.__traffic, Flow)):
			#update local component status
			self.__traffic.localPathComponentStatus[self.__traffic.getID] = Status.AVAILABLE
			if(self.__traffic.inUsePath == None):
				if(self.__traffic.isBackupPossible()): #based on local knowledge
					events.append(BackupEvent(self.getEventTime()+self.__traffic.getReactionTime(), self.__traffic))
				else:
					#backup not possible
					pass
			else:
				#flow already un-paused recovery message will not do anything
				pass
		else:
			raise NotImplementedError("Not implemented for other traffic classes yet")

		return events
	

class BackupEvent(Event):
	def __init__(self, eventTime, traffic, eventType= EventType.BACKUP):
		Event.__init__(self,eventTime, eventType)
		self.__traffic = traffic
	
	def handle(self):
		if(isinstance(self.__traffic,Flow)):
			if(self.__traffic.inUsePath is None):
				#attempt backup
				self.__traffic.inUsePath = self.__traffic.backup()
				if(self.__traffic.inUsePath is not None):
					#backup successful locally
					assert(self.__traffic.downFromTime is not None) #since flow was paused inititally, it could not have been getting service globally
					if(not self.__traffic.inUsePath.isFailed()):
						#backup successful globally as well
						self.__traffic.addDowntime(self.getEventTime() - self.__traffic.downFromTime)
						self.__traffic.downFromTime = None
					else:
						#backup unsuccessful globally, already not getting service so pass
						pass
				else:
					#backup unsuccessful
					pass
			else:
				#already un-paused no need for backup
				pass
		else:
			raise NotImplementedError("Not implemented for other traffic classes yet")

		return []

class ArrivalEvent(Event):
	#static variables
	totalRejects = 0
	totalAllocations = 0

	def __init__(self, _time, _eventType):
		Event.__init__(self, _time, _eventType)

	def handle(self):
		if(cfg.stopAfterRejects!=-1):
			if(ArrivalEvent.totalRejects>=cfg.stopAfterRejects): #stop after X rejects
				ArrivalEvent.totalRejects+=1
				return []
		traffic = None
		trafficInfo = characteristics.getTrafficCharacteristics()
		if(TrafficType.FLOW == cfg.defaultTrafficType):
			traffic = Flow(self.getEventTime(),trafficInfo.flowLength_us / 1000000, (trafficInfo.flowSize_bytes*8) / 1000000)
		# elif(TrafficType.TENANT == self.__trafficInformation.getTrafficType()):
		elif(TrafficType.TENANT == cfg.defaultTrafficType):
			# traffic = Tenant()
			traffic = Tenant("Tenant", self.getEventTime(), trafficInfo.duration, trafficInfo.VMs, trafficInfo.BW)
		else:
			raise NotImplementedError
		
		if(not traffic.initialize()):
			ArrivalEvent.totalRejects+=1
			return []
		
		ArrivalEvent.totalAllocations+=1
		ev = DepartureEvent(traffic.getEndTime(), EventType.DEPARTURE, traffic)
		return [ev]

class DepartureEvent(Event):
	def __init__(self, _time, _eventType, traffic):
		Event.__init__(self, _time, _eventType)
		self.__traffic = traffic

	def handle(self):
		self.__traffic.unInitialize()
		#TODO: add to the total downtime the downtime of the departing traffic, and to total desired time the desired time for the departing traffic
		return []


class EndEvent(Event):
	def __init__(self, _time, _eventType):
		Event.__init__(self, _time, _eventType)

	def handle(self):
		globals.metricLogger.info("Total traffic rejects: %s" % ArrivalEvent.totalRejects)
		globals.metricLogger.info("Total traffic allocations before the first reject: %s" % ArrivalEvent.totalAllocations)
		# #TODO: do the following somewhere else
		# totalDowntime = 0.0
		# totalDesiredUptime = 0.0
		# for traffic in globals.topologyInstance.getAllTraffic().values():
		# 	totalDowntime+=traffic.getDowntime(self.getEventTime())
		# 	assert(traffic.getStartTime()<cfg.simulationTime) #traffic should have started before the end of simulation
		# 	if(traffic.getEndTime()>=cfg.simulationTime):
		# 		totalDesiredUptime+= (cfg.simulationTime - traffic.getStartTime())
		# 	else:
		# 		totalDesiredUptime+= (traffic.getEndTime()-traffic.getStartTime())
		
		# globals.metricLogger.info("Total traffic downtime: %s" % totalDowntime)
		# if(totalDesiredUptime>0):
		# 	globals.metricLogger.info("Total percentage uptime: %s" % ((float(totalDesiredUptime-totalDowntime)/float(totalDesiredUptime))*100))
		# else:
		# 	globals.metricLogger.info("Total percentage uptime: %s" % (100+"(No Traffic)"))

		helper.populateLoggersWithSimulationInfo("Ending information:")

		return []
