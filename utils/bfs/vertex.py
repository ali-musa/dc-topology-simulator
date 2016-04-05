from base.device import *
from base.link import *
from base.path import *

class Vertex():
	"""Vertex class for BFS"""
	def __init__(self, device, predecessorLink = None, predecessorVertex = None):
		self.device = device
		self.predecessorLink = predecessorLink
		self.predecessorVertex = predecessorVertex
		self.color = "white"
		
	
	def getUnVisitedConnectionsWithAvailableBW(self, bw, graph):
		vertices = []
		for tuple in self.device.getLinksAndNeighbouringDevices():
			if(tuple[0].getMinAvailableBW()>=bw):
				vertex=graph.findVertexByDevice(tuple[1])
				assert (vertex is not None)
				if(vertex.color=="white"):
					vertex.color="gray"			# marks the node as currently being processed
					vertex.predecessorLink = tuple[0]
					vertex.predecessorVertex = self
					vertices.append(vertex)
		return vertices