import uuid
from base.enum import TrafficPriority
class Traffic:
	def __init__(self, startTime, duration, priority=TrafficPriority.NORMAL):
		#private members
		self.__id = uuid.uuid4()
		self.__startTime = startTime
		self.__duration = duration

		#public members
		self.priority = priority

# Utility functions
	#public methods
	
	def __str__(self):
		printString = '=========================='
		printString +='\nID:			  ' + str(self.getID())
		printString +='\nStart Time:	  ' + str(self.startTime)
		printString +='\nDuration:	      ' + str(self.duration)
		printString +='\nDuration:	      ' + str(self.duration)
		printString +='\nPriority:		  ' + str(self.priority)
		return printString

	def getEndTime(self):
		return (self.startTime + self.duration)
	def getID(self):
		return self.__id