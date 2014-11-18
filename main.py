from base.event import *
from base.enum import *

from topology.topology import *
from topology.fattree import *
from topology.jellyfish import *

from failure.failure import *
from reservation.tenant import *

import config as cfg

import random
import time
import traceback

# *** START OF LOGGING CONFIGURATIONS ***
import logging
logLevel = getattr(logging, cfg.logLevel.upper(), None)
logFilename = cfg.logFilename
if not isinstance(logLevel, int):
    raise ValueError('Invalid log level: %s' % logLevel)
# NOTE: append "%(asctime)s" to format attribute below for showing time of log message
# NOTE: append "%(levelname)s" to format attribute below for showing log level name
# NOTE: filemode='w' makes a new file every time. remove this parameter to continue writing to same file every time.
logging.basicConfig(format='%(levelname)s : %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logLevel, filename=logFilename, filemode='w')
# *** END OF LOGGING CONFIGURATIONS ***

topo = None
failureModel = None
simTime = cfg.SimulationTime
numRequests = cfg.NumberOfRequests
eventID = 0
events = []

def print_timing(func):
	def wrapper(*args, **kwargs):
		t1 = time.time()
		res = func(*args, **kwargs)
		t2 = time.time()
		diff = t2-t1
		if func.func_name == 'main':
			minutes = int(diff/60.0)
			seconds = diff - (minutes*60)
			logging.debug('The simulation took %0.3f ms = %d min and %0.3f sec\n' % (diff*1000, minutes, seconds))
		else:
			logging.debug('%s() took %0.3f ms' % (func.func_name, diff*1000.0))
		return res
	return wrapper

@print_timing
def createInstances():
	global topo
	global failureModel
	global simTime
	global numRequests
	topoType = cfg.DefaultTopology
	failureType = cfg.DefaultFailureModel

	try:
		if(cfg.OverrideDefaults):
			topology_type = raw_input("Type of topology to create: ")
			if topology_type == "FatTree" or topology_type == "f":
				topoType = TopologyType.FATTREE
			elif topology_type == "JellyFish" or topology_type == "j":
				topoType = TopologyType.JELLYFISH
			elif topology_type == "Custom" or topology_type == "c":
				topoType = TopologyType.CUSTOM
			
			failure_type = raw_input("Failure model to implement: ")
			if failure_type == "Phillipa" or failure_type == "p":
				failureType = FailureType.PHILLIPA
			
			simTime = int( raw_input("Simulation time (in sec): ") )
			numRequests = int(raw_input("Number of requests to generate: "))

		assert topoType in TopologyType
		assert failureType in FailureType
		assert simTime > 0
		assert numRequests >= 0

		if(TopologyType.FATTREE == topoType):
			topo = FatTree()
		elif(TopologyType.JELLYFISH == topoType):
			topo = JellyFish()
		elif(TopologyType.CUSTOM == topoType):
			topo = Topolgoy(topoType)

		if (FailureType.PHILLIPA  == failureType):
			failureModel = Phillipa()

	except:
	 	logging.error("Invalid input! Exiting...")
	 	topo = None
	 	failureModel = None
	 	simTime = None
	 	numRequests = None
	 	traceback.print_exc()


def initializeSimulator():
	global eventID
	global events
	# generate topology
	topo.generate()
	# initialize failure model
	failureModel.initialize(topo.getDevices(), topo.getLinks(), simTime)
	# create the end event
	events = []
	end = EndEvent(0, simTime, EventType.END)
	events.append(end)
	eventID = 1
	# create all failure events
	createIniFailures()
	# create all tenant events
	createIniRequests()


@print_timing
def main():
	global events
	random.seed(None)

	createInstances()
	
	# check if all user inputs have been taken
	if None in [topo, failureModel, simTime, numRequests]:
		return
	
	initializeSimulator()

	# topo.blah()
	data = dict()
	data["topo"] = topo
	data["failureModel"] = failureModel
	data["simTime"] = simTime
	data["lastID"] = eventID

	logging.info("Starting simulation!")

	tenant = Tenant("1", "Tenant 1", 1, 100, 100, 100)
	topo.oktopus(8,5, tenant)
	logging.debug(tenant)

	while events:
		event = events[0].handle(data)
		logging.debug(event)
		del events[0]
		sortedInsert(event)
		data["lastID"] = eventID

	logging.info("Ending simulation!")
	logging.info("Total number of events: " + str(eventID))


##### create initial set of failure events #####
def createIniFailures():
	logging.info('Generating device failures')
	devices = topo.getDevices()
	for _id,_device in devices.iteritems():
		event = createFailure(_id)
		sortedInsert(event)
	logging.info('Generating link failures')
	links = topo.getLinks()
	for _id,_link in links.iteritems():
		event = createFailure(_id)
		sortedInsert(event)

def createFailure(componentID):
	time = failureModel.createFailureTime(componentID)
	if time == -1:
		return None
	return FailureEvent(eventID, time, EventType.FAILURE, componentID)

##### create initial set of allocation events #####
def createIniRequests():
	logging.info('Generating tenant requests')
	for i in range(0, numRequests):
		event = createTenant()
		sortedInsert(event)

def createTenant():
	sampleTime1 = simTime / 4.0
	sampleTime2 = simTime / 2.0
	startTime = simTime*2
	while startTime > simTime:
		startTime = int(random.expovariate(1/sampleTime1))
	duration = int(random.expovariate(1/sampleTime2))
	vms = int(random.expovariate(1/49.0))
	bw = int(random.expovariate(1/100.0))
	if startTime < 1:
		startTime = 1
	if duration < 1:
		duration = 1
	if vms < 2:
		vms = 2
	if bw < 1:
		bw = 1
	return ArrivalEvent(eventID, startTime, EventType.ARRIVAL, vms, bw, duration)

##### sortedInsert an event into the list of events #####
def sortedInsert(event):
	global eventID
	global events
	if event is not None:
		time = event.getEventTime()
		numEvents = len(events)
		for i in range(numEvents):
			if events[i].getEventTime() > time:
				events.insert(i, event)
				eventID = eventID + 1
				break


if __name__ == '__main__':
	main()