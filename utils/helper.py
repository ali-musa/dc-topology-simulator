import time
import globals as globals
from bfs.queue import *
from bfs.vertex import *
from bfs.graph import *
from base.path import *
import gc

class helper():
	@staticmethod
	def print_timing(func):
		def wrapper(*args, **kwargs):
			t1 = time.time()
			res = func(*args, **kwargs)
			t2 = time.time()
			diff = t2 - t1
			if func.func_name == 'main':
				minutes = int(diff / 60.0)
				seconds = diff - (minutes * 60)
				globals.simulatorLogger.info('The simulation took %0.3f ms = %d min and %0.3f sec\n' % (diff * 1000, minutes, seconds))
			else:
				globals.simulatorLogger.debug('%s() took %0.3f ms' % (func.func_name, diff * 1000.0))
			return res
		return wrapper
	
	#takes in a source, destination objects, existing paths list and the bandwidth required
	#retuns the first shortest disjoint path with atleast the BW specified as an object of Path class, if such a path is found else returns None
	@staticmethod #reference http://interactivepython.org/courselib/static/pythonds/Graphs/graphbfs.html
	def findDisjointPathBFS(topology,source, destination, bandwidth = 0, existingPaths=[]):
		globals.simulatorLogger.info("Finding disjoint path from %s to %s" % (source.getID(), destination.getID()))
		bfsGraph = graph()
		bfsGraph.generate(topology)
		if(existingPaths):
			for path in existingPaths:
				for component in path.getComponents():
					if(isinstance(component, Device)):
						if(BackupStrategy.TOR_TO_TOR == cfg.defaultBackupStrategy):
							if((not component.isHost) and (component not in source.getNeighbouringDevices()) and (component not in destination.getNeighbouringDevices())): #avoid hosts and tor level components
								bfsGraph.findVertexByDevice(component).color = "black" #mark as visited
						elif(BackupStrategy.END_TO_END == cfg.defaultBackupStrategy):
							if(not component.isHost):
								bfsGraph.findVertexByDevice(component).color = "black" #mark as visited
						else:
							raise NotImplementedError("Not implemented for other backup strategies yet")
		start = bfsGraph.findVertexByDevice(source)
		end = bfsGraph.findVertexByDevice(destination)
		vertexQueue = Queue()
		vertexQueue.enqueue(start)
		while(vertexQueue.size() > 0):
			currentVert = vertexQueue.dequeue()
			globals.simulatorLogger.debug(currentVert.device.__str__())

			if currentVert.device == end.device:
				currentVert.color = "black"
				path = []
				while currentVert.predecessorVertex!= None:
					path.append(currentVert.device)
					path.append(currentVert.predecessorLink)
					currentVert = currentVert.predecessorVertex
				path.append(currentVert.device)
				path.reverse()
				pathClassObj = Path(path)
				globals.simulatorLogger.info("Shortest Disjoint path from %s to %s found. Hoplength %s" % (source.getID(), destination.getID(),pathClassObj.getHopLength()))
				del bfsGraph
				gc.collect() #force garbage collection
				return (pathClassObj)

			for nbr in currentVert.getUnVisitedConnectionsWithAvailableBW(bandwidth,bfsGraph):
				vertexQueue.enqueue(nbr)
			currentVert.color="black"			# the node has been visited
		globals.simulatorLogger.info("Unable to find disjoint path from %s to %s" % (source.getID(), destination.getID()))
		return None

	#prints any topology by running bfs on it
	@staticmethod
	def printTopology(topology):
		globals.simulatorLogger.info( "Starting BFS...")
		bfsGraph = graph()
		bfsGraph.generate(topology)
		start = bfsGraph.findVertexByDevice(topology.getDevices().values()[0])#start with the first device in the list
		vertQueue = Queue()
		vertQueue.enqueue(start)
		while(vertQueue.size() > 0):
			currentVert = vertQueue.dequeue()
			globals.simulatorLogger.info(currentVert.device.__str__())
			for nbr in currentVert.getUnVisitedConnectionsWithAvailableBW(0,bfsGraph):
				vertQueue.enqueue(nbr)
			currentVert.color="black"			# the node has been visited
		del bfsGraph
		gc.collect() #force garbage collection
		globals.simulatorLogger.info("Finished BFS on entire topology!")


	@staticmethod
	def sortedInsert(fromEvents, intoEvents):
	# this method is used to insert sorted events in the event queue on the basis of their time of occurence
		for event in fromEvents:
			currentEventTime = event.getEventTime()
			if(currentEventTime>cfg.simulationTime): #insert only if the event time is within the simulation end time
				globals.simulatorLogger.warning("Event beyond the simulation time, not adding it to the run queue:\n%s" % event.__str__())
				continue
			if event is not None:
				if intoEvents: #intoEvents are not empty
					numEvents = len(intoEvents)
					for i in range(numEvents):
						if intoEvents[i].getEventTime() > currentEventTime:
							intoEvents.insert(i, event)
							break
				else:
					intoEvents.append(event)


	@staticmethod
	def findValue(line, param):
	# this method is used while parsing custom topology input
		i = 0
		for l in line:
			if l == param:
				return line[i + 1]
			i+=1
		return None

	@staticmethod
	def populateLoggersWithSimulationInfo(str=None):
		if (str is not None):
			globals.metricLogger.info("%s" % str)
			globals.simulatorLogger.info("%s" % str)
		
		globals.metricLogger.info("%s" % globals.topologyInstance.__str__())
		globals.metricLogger.info("%s" % globals.failureModelInstance.__str__())
		globals.metricLogger.info("Simulation time: %s" % cfg.simulationTime)
		globals.metricLogger.info("Number of requests: %s" % cfg.numberOfRequests)
		globals.metricLogger.info("Allocation strategy: %s" % cfg.defaultAllocationStrategy)
		globals.metricLogger.info("Traffic type: %s" % cfg.defaultTrafficType)
		globals.metricLogger.info("Traffic characteristics: %s" % cfg.defaultTrafficCharacteristics)
		globals.metricLogger.info("Backup strategy: %s" % cfg.defaultBackupStrategy)
		globals.metricLogger.info("Number of backups: %s" % cfg.numberOfBackups)
		globals.metricLogger.info("Stop after rejects(-1 dont stop): %s" % cfg.stopAfterRejects)

		globals.simulatorLogger.info("%s" % globals.topologyInstance.__str__())
		globals.simulatorLogger.info("%s" % globals.failureModelInstance.__str__())
		globals.simulatorLogger.info("Simulation time: %s" % cfg.simulationTime)
		globals.simulatorLogger.info("Number of requests: %s" % cfg.numberOfRequests)
		globals.simulatorLogger.info("Allocation strategy: %s" % cfg.defaultAllocationStrategy)
		globals.simulatorLogger.info("Traffic type: %s" % cfg.defaultTrafficType)
		globals.simulatorLogger.info("Traffic characteristics: %s" % cfg.defaultTrafficCharacteristics)
		globals.simulatorLogger.info("Backup strategy: %s" % cfg.defaultBackupStrategy)
		globals.simulatorLogger.info("Number of backups: %s" % cfg.numberOfBackups)
		globals.simulatorLogger.info("Stop after rejects(-1 dont stop): %s" % cfg.stopAfterRejects)