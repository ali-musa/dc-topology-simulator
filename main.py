from base.event import *
from base.enum import *

from topology.topology import *
from topology.fattree import *
from topology.jellyfish import *

from failure.failure import *

import random
import time
import traceback

topo = None
failureModel = None
simTime = None
numRequests = None
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
			print 'The simulation took %0.3f ms = %d min and %0.3f sec\n' % (diff*1000, minutes, seconds)
		else:
			print '%s() took %0.3f ms' % (func.func_name, diff*1000.0)
		return res
	return wrapper

@print_timing
def getUserInput():
	global topo
	global failureModel
	global simTime
	global numRequests
	topoType = ""
	failureType = ""

	try:
		topology_type = raw_input("Type of topology to create: ")
		if topology_type == "FatTree" or topology_type == "f":
			topoType = TopologyType.FATTREE
			topo = FatTree()
		elif topology_type == "JellyFish" or topology_type == "j":
			topoType = TopologyType.JELLYFISH
			topo = JellyFish()
		elif topology_type == "Custom" or topology_type == "c":
			topoType = TopologyType.CUSTOM
			topo = Topology(topoType)
		# assert topoType in TopologyType

		failure_type = raw_input("Failure model to implement: ")
		if failure_type == "Phillipa" or failure_type == "p":
			failureType = Failure.PHILLIPA
			failureModel = Phillipa()
		assert failureType in Failure

		# sTime = ( raw_input("Simulation time (in sec): ") ).split(",")
		# simTime = int("".join(sTime))
		simTime = int( raw_input("Simulation time (in sec): ") )
		assert simTime > 0

		numRequests = int(raw_input("Number of requests to generate: "))
		assert numRequests >= 0
	except:
		print "Invalid input! Please try again. Exiting..."
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

	# to-do config file defaults
	print
	getUserInput()
	print
	
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

	print
	print "Starting simulation!"
		
	topo.printTopo()

	for _id, _l in topo.links.iteritems():
		print _l
	# for d in topo.devices:
		# print d
	
	# print topo.findPath("h_1_1_1", "t_4_2")

	# a12 = topo.devices["a_1_2"]
	# nbrs = a12.getNeighbours()
	# for n in nbrs:
	# 	print n

	while events:
		event = events[0].handle(data)
		print event
		del events[0]
		sortedInsert(event)
		data["lastID"] = eventID

	print "Ending simulation!"
	print
	print "Total number of events: " + str(eventID)
	print


##### create initial set of failure events #####
def createIniFailures():
	print 'Generating device failures'
	devices = topo.getDevices()
	for _id,_device in devices.iteritems():
		event = createFailure(_id)
		sortedInsert(event)
	print 'Generating link failures'
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
	print 'Generating tenant requests'
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