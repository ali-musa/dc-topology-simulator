from init import *

@helper.print_timing
def main():
	events = []
	
	print("Simulation started please wait!")
	globals.simulatorLogger.info("Starting simulation!")
	

	initialEvents = initializer.initializeSimulator()
	helper.sortedInsert(initialEvents,events)
	while events:
		if cfg.logEachEvent:
			globals.simulatorLogger.debug(events[0])
		newEvents = events[0].handle()
		del events[0]
		gc.collect() #force garbage collection
		helper.sortedInsert(newEvents, events)

	globals.simulatorLogger.info("Ending simulation!")
	print("Simulation ended!")

if __name__ == '__main__':
	main()