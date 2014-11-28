from failure.failure import *
from enum import *
import uuid
from reservation.tenant import *
from base.path import *
import logging
import globals as globals
from reservation import *
from reservation.flow import *
from reservation.tenant import *
from reservation.traffic import *
from exceptions import NotImplementedError


"""
eventType = "Failure" or "Recovery" or "Arrival" or "Departure" or "End"
"""

class Event:
	def __init__(self, _time, _eventType):
		self.id = uuid.uuid4()
		self.time = _time
		self.eventType = _eventType

	def getEventID(self):
		return self.id
	def getEventTime(self):
		return self.time
	def getEventType(self):
		return self.eventType

# over-loaded __str__() for print functionality
	def __str__(self):
		printString = "=========================="
		printString += "\nEvent Information"
		printString += "\n--------------------------"
		printString += "\nEvent ID: " + str(self.id)
		printString += "\nEvent Time: " + str(self.time)
		printString += "\nEvent Type: " + str(self.eventType)
		printString += "\n=========================="
		return printString


class FailureEvent(Event):
	def __init__(self, _time, _eventType, _objectID):
		Event.__init__(self, _time, _eventType)
		self.compID = _objectID

	def handle(self, data):
		topo = data["topo"]
		topo.failComponentById(self.compID)

		failureModel = data["failureModel"]
		ttR = failureModel.getTTR(self.compID)
		if ttR == -1:
			return []
		#simTime = data["simTime"]
		time = self.time + ttR
		#if simTime < time:
		#	return []
		ev = RecoveryEvent(time, EventType.RECOVERY, self.compID)

		##create backup event
		#if(traffic.detectionTime()+)


		return [ev]


class RecoveryEvent(Event):
	def __init__(self,_time, _eventType, _objectID):
		Event.__init__(self, _time, _eventType)
		self.compID = _objectID

	def handle(self, data):
		topo = data["topo"]
		topo.recoverComponentById(self.compID)

		failureModel = data["failureModel"]
		ttF = failureModel.getTTF(self.compID)
		if ttF == -1:
			return []
		#simTime = data["simTime"]
		time = self.time + ttF
		#if simTime < time:
		#	return []
		ev = FailureEvent(time, EventType.FAILURE, self.compID)
		return [ev]


class ArrivalEvent(Event):
	def __init__(self, _time, _eventType, _vms, _bw, _duration):
		Event.__init__(self, _time, _eventType)
		self.VMs = _vms
		self.BW = _bw
		self.duration = _duration

	def handle(self, data):
		traffic = None
		if(AllocationStrategy.FLOW == cfg.defaultAllocationStrategy):
			sourceID = random.choice(filter(lambda x:x.isHost==True,(globals.topologyInstance.getDevices().values()))).getID()
			destID = random.choice(filter(lambda x:x.isHost==True,(globals.topologyInstance.getDevices().values()))).getID()
			traffic = Flow(0,100,sourceID,destID,10) # TODO: get input arguments from some distribution
		elif(AllocationStrategy.OKTOPUS == cfg.defaultAllocationStrategy):
			#traffic = Tenant()
			raise NotImplementedError
			
		else:
			raise NotImplementedError
		
		if(not traffic.initialize()):
			return []
		
		ev = DepartureEvent(traffic.getEndTime(), EventType.DEPARTURE, traffic)
		return [ev]

class DepartureEvent(Event):
	def __init__(self, _time, _eventType, traffic):
		Event.__init__(self, _time, _eventType)
		self.__traffic = traffic

	def handle(self):
		self.__traffic.unInitialize()
		return []


class EndEvent(Event):
	def __init__(self, _time, _eventType):
		Event.__init__(self, _time, _eventType)

	def handle(self, data):
		return []
