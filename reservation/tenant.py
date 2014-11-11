from traffic import *

class Tenant(Traffic):
	def __init__(self, _id, _label, _time, _active, _vms, _bw):
		Traffic.__init__(self, _id, _label, _time, _active, _bw)
		self.numVMs = _vms
		self.VMs = []
		self.hosts = []
		self.links = []

	def addVM(self, vm):
		self.VMs.append(vm)

	def addHost(self, host):
		self.hosts.append(host)
