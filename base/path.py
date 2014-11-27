import uuid
from base.link import Link

class Path:
	def __init__(self,components):
		#private members
		self.__id = uuid.uuid4()
		self.__components = components #Typically should include the source component and destination component

# Utility functions
	def getID(self):
		return self.__id

	def append(self, component): #TODO: remove this function, clean fattree.py accordingly (unnecessary overhead)
		self.__components.append(component)

	def getComponents(self):
		return self.__components

	def getHopLength(self):
		hopLength = 0
		for component in self.__components:
			if isinstance(component, Link):
				hopLength+=1
		return hopLength

		
