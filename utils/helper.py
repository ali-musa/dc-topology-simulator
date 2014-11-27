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
				globals.simulatorLogger.debug('The simulation took %0.3f ms = %d min and %0.3f sec\n' % (diff * 1000, minutes, seconds))
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
							if((not component.isHost) and (component.label!="tor")):
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
	def sortedInsert(event, events):
	# this method is used to insert sorted events in the event queue on the basis of their time of occurence
		if event is not None:
			time = event.getEventTime()
			numEvents = len(events)
			for i in range(numEvents):
				if events[i].getEventTime() > time:
					events.insert(i, event)
					break


	@staticmethod
	def findValue(line, param):
	# this method is used while parsing custom topology input
		i = 0
		for l in line:
			if l == param:
				return line[i + 1]
			i+=1
		return None