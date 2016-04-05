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
		printString +='\nID:			  ' + str(self.__id)
		printString +='\nStart Time:	  ' + str(self.__startTime)
		printString +='\nDuration:	      ' + str(self.__duration)
		printString +='\nPriority:		  ' + str(self.priority)
		return printString

	def getEndTime(self):
		return (self.__startTime + self.__duration)
	def getStartTime(self):
		return self.__startTime
	def getID(self):
		return self.__id
