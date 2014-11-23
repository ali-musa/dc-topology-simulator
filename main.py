from init import *

topo = None
failureModel = None
simTime = cfg.SimulationTime
numRequests = cfg.NumberOfRequests
events = []

@helper.print_timing
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
			elif topology_type == "Nacre" or topology_type == "n":
				topoType = TopologyType.NACRE
			elif topology_type == "Custom" or topology_type == "c":
				topoType = TopologyType.CUSTOM
			
			failure_type = raw_input("Failure model to implement: ")
			if failure_type == "Phillipa" or failure_type == "p":
				failureType = FailureType.PHILLIPA
			
			simTime = int(raw_input("Simulation time (in sec): "))
			numRequests = int(raw_input("Number of requests to generate: "))

		assert topoType in TopologyType
		assert failureType in FailureType
		assert simTime > 0
		assert numRequests >= 0

		if(TopologyType.FATTREE == topoType):
			topo = FatTree()
		elif(TopologyType.JELLYFISH == topoType):
			topo = JellyFish()
		elif(TopologyType.NACRE == topoType):
			topo = Nacre()
		elif(TopologyType.CUSTOM == topoType):
			topo = Topolgoy(topoType)

		if (FailureType.PHILLIPA == failureType):
			failureModel = Phillipa()

	except:
		logging.error("Invalid input! Exiting...")
		topo = None
		failureModel = None
		simTime = None
		numRequests = None
		traceback.print_exc()


def initializeSimulator():
	global events
	# generate topology
	topo.generate()
	# initialize failure model
	failureModel.initialize(topo.getDevices(), topo.getLinks(), simTime)
	# create the end event
	events = []
	end = EndEvent(simTime, EventType.END)
	events.append(end)
	# create all failure events
	createIniFailures()
	# create all tenant events
	createIniRequests()


@helper.print_timing
def main():
	global events
	random.seed(None)

	createInstances()
	
	# check if all user inputs have been taken
	if None in [topo, failureModel, simTime, numRequests]:
		logging.error("Not all inputs correctly provided.")
		return
	
	initializeSimulator()

	data = dict()
	data["topo"] = topo
	data["failureModel"] = failureModel
	data["simTime"] = simTime

	logging.info("Starting simulation!")

	# tenant = Tenant("1", "Tenant 1", 1, 100, 100, 100)
	# topo.oktopus(8,5, tenant)
	# logging.debug(tenant)

	for tenant_number in range(1):
		# vms = random.randrange(k*(k/2)**2)
		vms = 12
		logging.debug("VMs: " + str(vms))
		bw = 46
		logging.debug("BW: " + str(bw))
		tenant = Tenant("Testing Tenant", 1, 100, 100, 100)
		# if topo.oktopus(vms,bw, tenant):

	while events:
		event = events[0].handle(data)
		#logging.debug(event)
		del events[0]
		sortedInsert(event)

	logging.info("Ending simulation!")


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
	return FailureEvent(time, EventType.FAILURE, componentID)

##### create initial set of allocation events #####
def createIniRequests():
	logging.info('Generating tenant requests')
	for i in range(0, numRequests):
		event = createTenant()
		sortedInsert(event)

def createTenant():
	sampleTime1 = simTime / 4.0
	sampleTime2 = simTime / 2.0
	startTime = simTime * 2
	while startTime > simTime:
		startTime = int(random.expovariate(1 / sampleTime1))
	duration = int(random.expovariate(1 / sampleTime2))
	vms = int(random.expovariate(1 / 49.0))
	bw = int(random.expovariate(1 / 100.0))
	if startTime < 1:
		startTime = 1
	if duration < 1:
		duration = 1
	if vms < 2:
		vms = 2
	if bw < 1:
		bw = 1
	return ArrivalEvent(startTime, EventType.ARRIVAL, vms, bw, duration)

##### sortedInsert an event into the list of events #####
def sortedInsert(event):
	global events
	if event is not None:
		time = event.getEventTime()
		numEvents = len(events)
		for i in range(numEvents):
			if events[i].getEventTime() > time:
				events.insert(i, event)
				break


if __name__ == '__main__':
	main()