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
		
	
	def getConnectionsWithAvailableBW(self, bw):
		vertices = []
		for tuple in self.device.getLinksAndNeighbouringDevices():
			if(tuple[0].getMinAvailableBW()>=bw):
				vertices.append(Vertex(tuple[1],tuple[0],self))
		return vertices