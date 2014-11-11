import link
import device

class Path:
	def __init__(self):
		self.id = 0
		self.label = "Hey"
		self.isPrimary = True
		self.beingUsed = not self.isPrimary
		self.components = []

# Utility functions
	def append(self, component):
		self.components.append(component)

	def getComponents(self):
		return self.components

	def getLength(self):
		return len(self.components)

		
