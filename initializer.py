from init import *
class initializer():

	@staticmethod
	def __createInstances():
		try:
			if(cfg.overrideDefaults):
				topology_type = raw_input("Type of topology to create: ")
				if topology_type == "FatTree" or topology_type == "f":
					cfg.defaultTopology = TopologyType.FATTREE
				elif topology_type == "JellyFish" or topology_type == "j":
					cfg.defaultTopology = TopologyType.JELLYFISH
				elif topology_type == "Nacre" or topology_type == "n":
					cfg.defaultTopology = TopologyType.NACRE
				elif topology_type == "Custom" or topology_type == "c":
					cfg.defaultTopology = TopologyType.CUSTOM
				
				failure_type = raw_input("Failure model to implement: ")
				if failure_type == "Phillipa" or failure_type == "p":
					cfg.defaultFailureModel = FailureType.PHILLIPA
				
				cfg.simulationTime = int(raw_input("Simulation time (in sec): "))
				cfg.numberOfRequests = int(raw_input("Number of requests to generate: "))

			assert cfg.defaultTopology in TopologyType
			assert cfg.defaultFailureModel in FailureType
			assert cfg.simulationTime > 0
			assert cfg.numberOfRequests >= 0

			if(TopologyType.FATTREE == cfg.defaultTopology):
				globals.topologyInstance = FatTree()
			elif(TopologyType.JELLYFISH == cfg.defaultTopology):
				globals.topologyInstance = JellyFish()
			elif(TopologyType.NACRE == cfg.defaultTopology):
				globals.topologyInstance = Nacre()
			elif(TopologyType.CUSTOM == cfg.defaultTopology):
				globals.topologyInstance = Topology(cfg.defaultTopology)

			if (FailureType.PHILLIPA == cfg.defaultFailureModel):
				globals.failureModelInstance = Phillipa()
			return True

		except:
			globals.simulatorLogger.error("Invalid input! Exiting...")
			traceback.print_exc()
			return False
		
	@staticmethod
	def __createIniFailures(failureModel,events):
		globals.simulatorLogger.info('Generating device failures')
		devices = globals.topologyInstance.getDevices()
		for _id,_device in devices.iteritems():
			event = initializer.__createFailureEvent(failureModel, _id)
			if event is not None:
				events.append(event)
		globals.simulatorLogger.info('Generating link failures')
		links = globals.topologyInstance.getLinks()
		for _id,_link in links.iteritems():
			event = initializer.__createFailureEvent(failureModel, _id)
			if event is not None:
				events.append(event)

	@staticmethod
	def __createFailureEvent(failureModel, componentID):
		time = failureModel.createFailureTime(componentID)
		if time == -1:
			return None
		return FailureEvent(time, EventType.FAILURE, componentID)

	@staticmethod
	def __createIniRequests(events):
		if TrafficType.FLOW == cfg.defaultTrafficType:
			globals.simulatorLogger.info('Creating flow arrival events')
			for request in range(cfg.numberOfRequests):
				event = initializer.__createRandomUniformArrival()
				if event is not None:
						events.append(event)
					
		elif TrafficType.TENANT == cfg.defaultTrafficType:
			globals.simulatorLogger.info('Creating tenant arrival events')
			for i in range(0, cfg.numberOfRequests):
				event = initializer.__createTenant(cfg.simulationTime)
				if event is not None:
					events.append(event)

	@staticmethod
	def __createTenant(simTime): #TODO: move this distribution to traffic.characteristics module
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
		return ArrivalEvent(startTime, EventType.ARRIVAL)#, vms, bw, duration)

	@staticmethod
	def __createRandomUniformArrival():
		return ArrivalEvent(random.randint(0,cfg.simulationTime), EventType.ARRIVAL)

	@staticmethod
	def initializeSimulator():
		if(not initializer.__createInstances()):
			return []
		# generate topology
		globals.topologyInstance.generate()
		# initialize failure model
		globals.failureModelInstance.initialize(globals.topologyInstance.getDevices(), globals.topologyInstance.getLinks(), cfg.simulationTime)
		
		helper.populateLoggersWithSimulationInfo("Starting information:")

		# create the end event
		events = []
		end = EndEvent(cfg.simulationTime, EventType.END)
		if end is not None:
			events.append(end)
		# create all failure events
		initializer.__createIniFailures(globals.failureModelInstance, events) 
		# create all tenant events
		initializer.__createIniRequests(events)
		return events