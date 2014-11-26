from traffic import *

class Tenant(Traffic):
	def __init__(self, _label, _time, _active, _vms, _bw):
		Traffic.__init__(self, _label, _time, _active, _bw)
		self.numVMs = _vms
		self.VMs = []
		self.hostsAndNumVMs = dict() # dict of tuples <host, numVMs of this tenant in that host>
		self.linksAndBw = dict() # dict of tuples <link, BW reserved for this tenant on that link>

	def addVM(self, vm):
		self.VMs.append(vm)

	def addHost(self, host, numVMs):
		self.hostsAndNumVMs[host.getID()] = [host, numVMs]

	def addLink(self, link, bw):
		self.linksAndBw[link.getID()] = [link, bw]

	def getHostsAndNumVMs(self):
		return self.hostsAndNumVMs

	def getLinksAndBw(self):
		return self.linksAndBw

	def getVMs(self):
		return self.VMs

	# over-loaded __str__() for print functionality
	def __str__(self):
		printString =  "=========================="
		printString += "\nTenant Information"
		printString += "\n--------------------------"
		printString += "\nID:           " + str(self.id)
		printString += "\nLabel:        " + str(self.label)
		printString += "\nTime:         " + str(self.time)
		printString += "\nActive Time:  " + str(self.activeTime)
		printString += "\nEnd Time:     " + str(self.endTime)
		printString += "\nBandwidth:    " + str(self.bw)
		printString += "\nHosts: "
		for hostID, data in self.hostsAndNumVMs.iteritems():
			printString += "\nVMs:          " + str(data[1]) + " in Host:         " + str(data[0].getID())
		printString += "\nLinks: "
		for linkID, data in self.linksAndBw.iteritems():
			printString += "\nBW:          " + str(data[1]) + " on Link:         " + str(data[0].getID())	
		printString +=  "\n=========================="
		return printString