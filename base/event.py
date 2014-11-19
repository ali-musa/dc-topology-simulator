from failure.failure import *
from enum import *

"""
eventType = "Failure" or "Recovery" or "Arrival" or "Departure" or "End"
"""

class Event:
	def __init__(self, _id, _time, _eventType):
		self.id = _id
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
	def __init__(self, _id, _time, _eventType, _object):
		Event.__init__(self, _id, _time, _eventType)
		self.compID = _object

	def handle(self, data):
		topo = data["topo"]
		topo.failComponent(self.compID)

		failureModel = data["failureModel"]
		ttR = failureModel.getTTR(self.compID)
		if ttR == -1:
			return None
		simTime = data["simTime"]
		time = self.time + ttR
		if simTime < time:
			return None

		lastID = data["lastID"]
		id = lastID + 1
		ev = RecoveryEvent(id, time, EventType.RECOVERY, self.compID)
		return ev


class RecoveryEvent(Event):
	def __init__(self, _id, _time, _eventType, _object):
		Event.__init__(self, _id, _time, _eventType)
		self.compID = _object

	def handle(self, data):
		topo = data["topo"]
		topo.recoverComponent(self.compID)

		failureModel = data["failureModel"]
		ttF = failureModel.getTTF(self.compID)
		if ttF == -1:
			return None
		simTime = data["simTime"]
		time = self.time + ttF
		if simTime < time:
			return None

		lastID = data["lastID"]
		id = lastID + 1
		ev = FailureEvent(id, time, EventType.FAILURE, self.compID)
		return ev


class ArrivalEvent(Event):
	def __init__(self, _id, _time, _eventType, _vms, _bw, _duration):
		Event.__init__(self, _id, _time, _eventType)
		self.tenantID = _id
		self.VMs = _vms
		self.BW = _bw
		self.duration = _duration

	def handle(self, data):
		topo = data["topo"]
		if not topo.allocate(self.tenantID, self.VMs, self.BW):
			return None

		simTime = data["simTime"]
		time = self.time + self.duration
		if simTime < time:
			return None

		lastID = data["lastID"]
		id = lastID + 1
		ev = DepartureEvent(id, time, EventType.DEPARTURE, self.tenantID)
		return ev


class DepartureEvent(Event):
	def __init__(self, _id, _time, _eventType, _tenantID):
		Event.__init__(self, _id, _time, _eventType)
		self.tenantID = _tenantID

	def handle(self, data):
		topo = data["topo"]
		topo.deallocate(self.tenantID)
		return None


class EndEvent(Event):
	def __init__(self, _id, _time, _eventType):
		Event.__init__(self, _id, _time, _eventType)

	def handle(self, data):
		return None
