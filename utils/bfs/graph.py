from vertex import *
class graph():
	"""description of class"""
	def __init__(self):
		self.nodes = dict()
	def generate(self,topology):
		for device in topology.getDevices().values(): 
			self.nodes[device]=Vertex(device)
	def findVertexByDevice(self, device):
		return self.nodes[device]