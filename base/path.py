import link
import device
import uuid

class Path:
	def __init__(self):
		self.id = uuid.uuid4()
		self.components = []

# Utility functions
	def getID(self):
		return self.id

	def append(self, component):
		self.components.append(component)

	def getComponents(self):
		return self.components

	def getLength(self): #TODO: fix this function, the length of components list would not give the hop length
		return len(self.components)

	