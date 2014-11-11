import sys, os.path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from base.enum import *

import math
import random
import config as cfg

class FailureModel():
	def __init__(self, _failureModel):
		self.failureModel = _failureModel
		self.totalTime = 0


class Phillipa(FailureModel):
	def __init__(self):
		FailureModel.__init__(self, FailureType.PHILLIPA)
		self.failureClass = dict()
		self.proneDevices = 0
		self.proneLinks = 0

# over-loaded __str__() for print functionality
	def __str__(self):
		printString =  "=========================="
		printString += "\nFailure Information"
		printString += "\n--------------------------"
		printString += "\nFailure Model: " + str(self.failureModel)
		printString += "\nProne devices: " + str(self.proneDevices)
		printString += "\nProne links:   " + str(self.proneLinks)
		printString += "\n=========================="
		return printString


	def initialize(self, devices, links, _totalTime):
		self.totalTime = _totalTime
		types = ["tor", "aggr", "core"]
		resiliences = [cfg.ToRResilience, cfg.AggregatorResilience, cfg.CoreResilience]

		for i in range(3):
			ty = types[i]
			comps = self.getComponentSpecial(devices, ty)
			if len(comps) > 0:
				self.proneDevices = self.assignClass(comps, resiliences[i], self.proneDevices)

		for i in range(3):
			ty = types[i] + "Link"
			comps = self.getComponentSpecial(links, ty)
			if len(comps) > 0:
				self.proneLinks = self.assignClass(comps, resiliences[i], self.proneLinks)


	def getComponentSpecial(self, components, ty):
		return {_id: _comp for _id, _comp in components.iteritems() if _comp.getLabel() == ty}


	def assignClass(self, components, resilience, prone):
		num = len(components)
		a_size = num*(1.0-resilience)
		b_size = math.ceil(num*(resilience/2.0))
		c_size = math.ceil(num*(resilience/2.0))
		prone = prone + b_size + c_size

		while c_size:
			_id = random.choice(components.keys())
			self.failureClass[_id] = (components[_id], 2)
			del components[_id]
			c_size = c_size - 1
		while b_size:
			_id = random.choice(components.keys())
			self.failureClass[_id] = (components[_id], 1)
			del components[_id]
			b_size = b_size - 1
		return prone


	def createFailureTime(self, componentID):
		try:
			(comp, failClass) = self.failureClass[componentID]
			return random.randrange(self.totalTime)
		except:
			pass
		return -1


	def getTTR(self, _id):
		try:
			(component, failClass) = self.failureClass[_id]
			if failClass == 1:
				del self.failureClass[_id]
			compType = component.getType()
			compLabel = component.getLabel()
			val = random.randrange(100)
			if compType == CompType.DEVICE:
				if compLabel == "tor":
					return self.getTTR_ToR(val)
				if compLabel == "aggr":
					return self.getTTR_Aggr(val)
				if compLabel == "core":
					return self.getTTR_Core(val)
			elif compType == CompType.LINK:
				return self.getTTR_Link(val)
		except:
			pass
		return -1

	def getTTF(self, _id):
		try:
			(component, failClass) = self.failureClass[_id]
			compType = component.getType()
			compLabel = component.getLabel()
			val = random.randrange(100)
			if compType == CompType.DEVICE:
				if compLabel == "tor":
					return self.getTTF_ToR(val)
				if compLabel == "aggr":
					return self.getTTF_Aggr(val)
				if compLabel == "core":
					return self.getTTF_Core(val)
			elif compType == CompType.LINK:
				if compLabel == "torLink" or compLabel == "aggrLink":
					return self.getTTF_PodLink(val)
				if compLabel == "coreLink":
					return self.getTTF_CoreLink(val)
		except:
			pass
		return -1

###########################################################
####### Helper functions to get the time-to-failure #######
###########################################################
	def getTTF_ToR(self, val):
		if val < 8:
			return random.randrange(5, 5*60)
		elif val < 20:
			return random.randrange(5*60, 1000)
		elif val < 40:
			return random.randrange(1000, 60*60)
		elif val < 50:
			return random.randrange(60*60, 17782)
		elif val < 60:
			return random.randrange(17782, 24*60*60)
		elif val < 70:
			return random.randrange(24*60*60, 316227)
		elif val < 80:
			return random.randrange(316227, 7*24*60*60)
		elif val < 90:
			return random.randrange(7*24*60*60, 1995262)
		elif val < 100:
			return random.randrange(1995262, 10000000)

	def getTTF_Aggr(self, val):
		if val < 2:
			return random.randrange(5, 100)
		elif val < 30:
			return random.randrange(100, 5*60)
		elif val < 40:
			return random.randrange(5*60, 60*60)
		elif val < 65:
			return random.randrange(60*60, 24*60*60)
		elif val < 82:
			return random.randrange(24*60*60, 7*24*60*60)
		elif val < 100:
			return random.randrange(7*24*60*60, 3162277)

	def getTTF_Core(self, val):
		if val < 2:
			return random.randrange(5, 100)
		elif val < 45:
			return random.randrange(100, 1000)
		elif val < 70:
			return random.randrange(1000, 60*60)
		elif val < 100:
			return random.randrange(60*60, 10000000)

	def getTTF_PodLink(self, val):
		if val < 20:
			return random.randrange(100, 5*60)
		elif val < 40:
			return random.randrange(5*60, 1000)
		elif val < 60:
			return random.randrange(1000, 60*60)
		elif val < 70:
			return random.randrange(60*60, 50118)
		elif val < 82:
			return random.randrange(50118, 7*24*60*60)
		elif val < 91:
			return random.randrange(7*24*60*60, 1995262)
		elif val < 100:
			return random.randrange(1995262, 7000000)

	def getTTF_CoreLink(self, val):
		if val < 20:
			return random.randrange(100, 5*60)
		elif val < 40:
			return random.randrange(5*60, 60*60)
		elif val < 63:
			return random.randrange(60*60, 24*60*60)
		elif val < 67:
			return random.randrange(24*60*60, 7*24*60*60)
		elif val < 80:
			return random.randrange(7*24*60*60, 1000000)
		elif val < 90:
			return random.randrange(1000000, 3162277)
		elif val < 100:
			return random.randrange(3162277, 10000000)

###########################################################
####### Helper functions to get the time-to-recover #######
###########################################################
	def getTTR_ToR(self, val):
		if val < 40:
			return random.randrange(100, 5*60)
		elif val < 50:
			return random.randrange(5*60, 20*60)
		elif val < 80:
			return random.randrange(20*60, 60*60)
		elif val < 90:
			return random.randrange(60*60, 10000)
		elif val < 98:
			return random.randrange(10000, 24*60*60)
		elif val < 100:
			return random.randrange(24*60*60, 7*24*60*60)

	def getTTR_Aggr(self, val):
		if val < 20:
			return random.randrange(100, 5*60)
		elif val < 80:
			return random.randrange(5*60, 562)
		elif val < 90:
			return random.randrange(562, 1000)
		elif val < 97:
			return random.randrange(1000, 60*60)
		elif val < 100:
			return random.randrange(60*60, 10000)

	def getTTR_Core(self, val):
		if val < 50:
			return random.randrange(100, 5*60)
		elif val < 70:
			return random.randrange(5*60, 1000)
		elif val < 100:
			return random.randrange(1000, 7*24*60*60)

	def getTTR_Link(self, val):
		if val < 20:
			return random.randrange(100, 171)
		elif val < 40:
			return random.randrange(171, 251)
		elif val < 60:
			return random.randrange(251, 5*60)
		elif val < 80:
			return random.randrange(5*60, 400)
		elif val < 90:
			return random.randrange(400, 1000)
		elif val < 95:
			return random.randrange(1000, 60*60)
		elif val < 98:
			return random.randrange(60*60, 24*60*60)
		elif val < 100:
			return random.randrange(24*60*60, 7*24*60*60)