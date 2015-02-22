import random
from collections import namedtuple
import globals as globals
import config as cfg
from base.enum import *
from exceptions import NotImplementedError

class characteristics():
	"""Models traffic arrival departure and other characteristics"""
	@staticmethod
	def getTrafficCharacteristics():
		if(TrafficCharacteristics.UNIFORM_RANDOM == cfg.defaultTrafficCharacteristics):
			if(TrafficType.FLOW == cfg.defaultTrafficType):
				return characteristics.__getUniformInfiniteFlowCharacteristics()
			else:
				raise NotImplementedError("Uniform Random not implemented for other traffic types")
		elif(TrafficCharacteristics.EXPONENTIAL == cfg.defaultTrafficCharacteristics):
			if(TrafficType.TENANT == cfg.defaultTrafficType):
				return characteristics.__getExponentialTenantCharacteristics()
			else:
				raise NotImplementedError("Exponential not implemented for other traffic types")
		else:
			raise NotImplementedError("Not implemented for other distributions")

	@staticmethod
	def __getUniformFlowCharacteristics():
		#ref: Network Traffic Characteristics of DCs in the Wild
		flowCharacteristics = namedtuple("flowCharacteristics", "interarrivalTime_us flowSize_bytes flowLength_us")
		interarrivalTime_us = random.randrange(10,100000) #interarrival time in microseconds per switch
		flowSize_bytes = random.randrange(25, 100000000)
		flowLength_us = random.randrange(10,1000000000) #this flow length depends on the network (should probably not be used!)
		return(flowCharacteristics(interarrivalTime_us, flowSize_bytes, flowLength_us))

	@staticmethod
	def __getUniformInfiniteFlowCharacteristics():
		#ref: Network Traffic Characteristics of DCs in the Wild
		flowCharacteristics = namedtuple("flowCharacteristics", "interarrivalTime_us flowSize_bytes flowLength_us")
		interarrivalTime_us = random.randrange(10,100000) #interarrival time in microseconds per switch
		flowSize_bytes = random.randrange(25, 100000000)
		flowLength_us = (cfg.simulationTime+1)*1000000 #beyond simulation time to make flows infinite
		return(flowCharacteristics(interarrivalTime_us, flowSize_bytes, flowLength_us))

	@staticmethod
	def __getExponentialTenantCharacteristics():
		flowCharacteristics = namedtuple("flowCharacteristics", "VMs BW duration")
		vms = int(random.expovariate(1 / cfg.meanExpoVMs))
		bw = int(random.expovariate(1 / cfg.meanExpoBW))
		sampleTime = cfg.simulationTime / 2.0
		duration = int(random.expovariate(1 / sampleTime))
		if duration < 1:
			duration = 1
		if vms < 2:
			vms = 2
		if bw < 1:
			bw = 1
		return(flowCharacteristics(vms, bw, duration))		