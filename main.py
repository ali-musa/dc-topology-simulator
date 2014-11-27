from initializer import *

@helper.print_timing
def main():
	events = []
	random.seed(None)

	instances = initializer.createInstances()
	failureModel = instances[0]
	simTime = instances[1]
	numRequests = instances[2]

	# check if all user inputs have been taken
	if None in [globals.topologyInstance, failureModel, simTime, numRequests]:
		globals.simulatorLogger.error("Not all inputs correctly provided.")
		return

	data = dict()
	data["topo"] = globals.topologyInstance
	data["failureModel"] = failureModel
	data["simTime"] = simTime
	
	initializer.initializeSimulator(events, failureModel, simTime, numRequests)

	globals.simulatorLogger.info("Starting simulation!")

	while events:
		if cfg.logEachEvent:
			logging.debug(events[0])
		newEvents = events[0].handle(data)
		del events[0]
		for event in newEvents:
			helper.sortedInsert(event, events)

	globals.simulatorLogger.info("Ending simulation!")

if __name__ == '__main__':
	main()