from initializer import *

@helper.print_timing
def main():
	events = []
	random.seed(None)

	instances = initializer.createInstances()
	
	topo = instances[0]
	failureModel = instances[1]
	simTime = instances[2]
	numRequests = instances[3]

	# check if all user inputs have been taken
	if None in [topo, failureModel, simTime, numRequests]:
		logging.error("Not all inputs correctly provided.")
		return

	data = dict()
	data["topo"] = topo
	data["failureModel"] = failureModel
	data["simTime"] = simTime

	initializer.initializeSimulator(events, topo, failureModel, simTime, numRequests)

	logging.info("Starting simulation!")

	while events:
		event = events[0].handle(data)
		if cfg.logEachEvent:
			logging.debug(event)
		del events[0]
		helper.sortedInsert(event, events)

	logging.info("Ending simulation!")


if __name__ == '__main__':
	main()