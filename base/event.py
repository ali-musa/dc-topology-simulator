from failure.failure import *
from enum import *
import uuid
from reservation.tenant import *


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
			return None
		simTime = data["simTime"]
		time = self.time + ttR
		if simTime < time:
			return None
		ev = RecoveryEvent(time, EventType.RECOVERY, self.compID)
		return ev


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
			return None
		simTime = data["simTime"]
		time = self.time + ttF
		if simTime < time:
			return None
		ev = FailureEvent(time, EventType.FAILURE, self.compID)
		return ev


class ArrivalEvent(Event):
	def __init__(self, _time, _eventType, _vms, _bw, _duration):
		Event.__init__(self, _time, _eventType)
		self.VMs = _vms
		self.BW = _bw
		self.duration = _duration
		# Traffic ID to give to corresponding departure event
		self.trafficID = None
	def handle(self, data):
		topo = data["topo"]
		# if not topo.allocate(self.tenantID, self.VMs, self.BW): #TODO: implement this function correctly
		# 	return None
		tenant = Tenant("Tenant", self.time, self.duration, self.VMs, self.BW)
		if not topo.oktopus(self.VMs, self.BW, tenant):
			return None
		# add the generated traffic to the list of traffics in topology
		topo.addTraffic(tenant)
		# add this traffic to the event
		self.trafficID = tenant.getID()
		
		simTime = data["simTime"]
		time = self.time + self.duration
		if simTime < time:
			return None
		ev = DepartureEvent(time, EventType.DEPARTURE, self.trafficID)
		return ev

class DepartureEvent(Event):
	def __init__(self, _time, _eventType, _trafficID):
		Event.__init__(self, _time, _eventType)
		self.trafficID = _trafficID

	def handle(self, data):
		topo = data["topo"]
		assert topo.deallocate(self.trafficID)
		return None


class EndEvent(Event):
	def __init__(self, _time, _eventType):
		Event.__init__(self, _time, _eventType)

	def handle(self, data):
		return None
