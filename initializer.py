from init import *

class initializer():

	@staticmethod
	def createInstances():
		failureModel = cfg.defaultFailureModel
		simTime = cfg.simulationTime
		numRequests = cfg.numberOfRequests
		topoType = cfg.defaultTopology
		failureType = cfg.defaultFailureModel

		try:
			if(cfg.overrideDefaults):
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
				globals.topologyInstance = FatTree()
			elif(TopologyType.JELLYFISH == topoType):
				globals.topologyInstance = JellyFish()
			elif(TopologyType.NACRE == topoType):
				globals.topologyInstance = Nacre()
			elif(TopologyType.CUSTOM == topoType):
				globals.topologyInstance = Topology(topoType)

			if (FailureType.PHILLIPA == failureType):
				failureModel = Phillipa()

			return [failureModel, simTime, numRequests]

		except:
			globals.simulatorLogger.error("Invalid input! Exiting...")
			globals.topologyInstance = None
			failureModel = None
			simTime = None
			numRequests = None
			traceback.print_exc()

	@staticmethod
	def createIniFailures(events, failureModel):
		globals.simulatorLogger.info('Generating device failures')
		devices = globals.topologyInstance.getDevices()
		for _id,_device in devices.iteritems():
			event = initializer.createFailure(failureModel, _id)
			helper.sortedInsert(event, events)
		globals.simulatorLogger.info('Generating link failures')
		links = globals.topologyInstance.getLinks()
		for _id,_link in links.iteritems():
			event = initializer.createFailure(failureModel, _id)
			helper.sortedInsert(event, events)

	@staticmethod
	def createFailure(failureModel, componentID):
		time = failureModel.createFailureTime(componentID)
		if time == -1:
			return None
		return FailureEvent(time, EventType.FAILURE, componentID)

	@staticmethod
	def createIniRequests(numRequests, simTime, events):
		globals.simulatorLogger.info('Generating tenant requests')
		for i in range(0, numRequests):
			event = initializer.createTenant(simTime)
			helper.sortedInsert(event, events)

	@staticmethod
	def createTenant(simTime):
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

	@staticmethod
	def initializeSimulator(events,failureModel, simTime, numRequests):
		# generate topology
		globals.topologyInstance.generate()
		# initialize failure model
		failureModel.initialize(globals.topologyInstance.getDevices(), globals.topologyInstance.getLinks(), simTime)
		# create the end event
		# events = []
		end = EndEvent(simTime, EventType.END)
		events.append(end)
		# create all failure events
		initializer.createIniFailures(events, failureModel)
		# create all tenant events
		initializer.createIniRequests(numRequests, simTime, events)
