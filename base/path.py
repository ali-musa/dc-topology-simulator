import uuid
from base.link import Link
from base.enum import Status

class Path:
	def __init__(self,components, priority=0):
		#private members
		self.__id = uuid.uuid4()
		self.__components = components #Typically should include the source component and destination component (this is a list)
		self.__priority = priority

	def __str__(self):
		printString="==========================\nPath Information\n--------------------------\nPath ID: " +  str(self.__id)
		for component in self.__components:
			printString += "\nComponent ID: " + str(component.getID())
		printString += "\n=========================="
		return printString

# Utility functions
	def getID(self):
		return self.__id

	def append(self, component): #TODO: remove this function, clean fattree.py accordingly (unnecessary overhead)
		self.__components.append(component)
		
	def removeComponents(self,components):
		for component in components:
			self.__components.remove(component)

	def getComponents(self):
		return self.__components

	def getHopLength(self):
		hopLength = 0
		for component in self.__components:
			if isinstance(component, Link):
				hopLength+=1
		return hopLength

	def getPriority(self):
		return self.__priority
		
	def isFailed(self):
		for component in self.__components:
			if component.getStatus() == Status.FAIL:
				return True
		return False

	
	def getOverlappingLinks(self,path):
		overlappingLinks = []
		if path is None:
			return overlappingLinks
		selfComponents = self.getComponents()
		for component in path.getComponents():
			if isinstance(component, Link):
				for selfComponent in selfComponents:
					if component is selfComponent:
						overlappingLinks.append(component)
						break
		
		return overlappingLinks
