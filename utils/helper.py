import time
import globals as globals
from bfs.queue import *
from bfs.vertex import *
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
	
	#takes in a source, destination objects and the bandwidth required
	#retuns the first shortest path with atleast the BW specified as an object of Path class, if such a path is found else returns None
	@staticmethod #reference http://interactivepython.org/courselib/static/pythonds/Graphs/graphbfs.html
	def findShortestPathBFS(source, destination, bandwidth = 0):
		globals.simulatorLogger.info("Finding shortest path from %s to %s" % (source.getID(), destination.getID()))
		
		start = Vertex(source)
		end = Vertex(destination)
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
				globals.simulatorLogger.info("Shortest path from %s to %s found. Hoplength %s" % (source.getID(), destination.getID(),pathClassObj.getHopLength()))
				gc.collect() #force garbage collection
				return (pathClassObj)

			for nbr in currentVert.getConnectionsWithAvailableBW(bandwidth):
				if nbr.color == "white":		# the node is not yet visited
					nbr.color="gray"			# marks the node as currently being processed
					nbr.predecessorVertex = currentVert
					vertexQueue.enqueue(nbr)
			currentVert.color="black"			# the node has been visited
		return None

	#prints any topology by running bfs on it
	@staticmethod
	def printTopology(self,graph):
		globals.simulatorLogger.info( "Starting BFS...")
		
		start = Vertex(graph.devices[0])
		vertQueue = Queue()
		vertQueue.enqueue(start)
		while(vertQueue.size() > 0):
			currentVert = vertQueue.dequeue()
			globals.simulatorLogger.info(currentVert)
			for nbr in currentVert.getConnectionsWithAvailableBW(0):
				if nbr.color == "white":		# the node is not yet visited
					nbr.color="gray"			# marks the node as currently being processed
					nbr.predecessorVertex = currentVert
					vertexQueue.enqueue(nbr)
			currentVert.color="black"			# the node has been visited
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