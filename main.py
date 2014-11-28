from initializer import *

@helper.print_timing
def main():
	events = []
	random.seed(None)

	instances = initializer.createInstances()
	failureModel = instances[0]
	simulationTime = instances[1]
	numRequests = instances[2]

	# check if all user inputs have been taken
	if None in [globals.topologyInstance, failureModel, simulationTime, numRequests]:
		globals.simulatorLogger.error("Not all inputs correctly provided.")
		return

	data = dict()
	data["topo"] = globals.topologyInstance
	data["failureModel"] = failureModel
	
	initializer.initializeSimulator(events, failureModel, simulationTime, numRequests)

	globals.simulatorLogger.info("Starting simulation!")

	while events:
		if cfg.logEachEvent:
			logging.debug(events[0])
		newEvents = events[0].handle(data)
		del events[0]
		gc.collect() #force garbage collection
		for event in newEvents:
			if event.getEventTime() <= simulationTime:  #insert only if the event is within the simulation time
				helper.sortedInsert(event, events)

	globals.simulatorLogger.info("Ending simulation!")

if __name__ == '__main__':
	main()