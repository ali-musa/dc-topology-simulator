from topology import *

class FatTree(Tree):
	def __init__(self):
		Tree.__init__(self, TopologyType.FATTREE)
		self.k = 0
		self.bw = 1000
		self.VMsInHost = 8
		self.VMsInRack = 0
		self.VMsInPod = 0
		self.VMsInDC = 0

		self.availabilityUnderHosts = dict()
		self.availabilityUnderRacks = dict()
		self.availabilityUnderPods = dict()
		self.availabilityUnderDC = (0, self.bw)

# over-loaded __str__() for print functionality
	def __str__(self):
		printString =  "=========================="
		printString += "\nTopology Information"
		printString += "\n--------------------------"
		printString += "\nTopology:    " + str(self.topologyType)
		printString += "\nk:           " + str(self.k)
		printString += "\nDevices:     " + str(len(self.devices))
		printString += "\nLinks:       " + str(len(self.links))
		printString += "\nAllocations: " + str(len(self.allocations))
		printString += "\nFree VMs:    " + str(self.availabilityUnderDC[0])
		printString += "\n=========================="
		return printString


	def generate(self):
		try:
			self.k = int(raw_input("Enter value of k: "))
			assert (self.k > 0) and (self.k%2 == 0)
		except:
			print "Invalid inputs! Please try again. Exiting..."
			return None

		print
		print "Generating " + str(self.k) + "-ary FatTree topology"
		self.VMsInRack = self.VMsInHost * self.k / 2
		self.VMsInPod = self.VMsInRack * self.k / 2
		self.VMsInDC = self.VMsInPod * self.k
		# initialize lists
		cores = []
		aggrs = []
		tors = []
		hosts = []
		# add (k/2)^2 cores
		for c in range(self.k*self.k/4):
			coreName = "c_" + str(c+1)
			core = Device(coreName, "core", False)
			cores.append(core)
		# add pods with k/2 aggrs and k/2 tors, with k/2 hosts per tor
		for pod in range(self.k):
			for sw in range(self.k/2):
				aggrName = "a_" + str(pod+1) + "_" + str(sw+1)
				torName = "t_" + str(pod+1) + "_" + str(sw+1)
				aggr = Device(aggrName, "aggr", False)
				tor = Device(torName, "tor", False)
				for h in range(self.k/2):
					hostName = "h_" + str(pod+1) + "_" + str(sw+1) + "_" + str(h+1)
					host = Device(hostName, "host", True)
					linkName = host.getID()+"+"+tor.getID()
					hostLink = Link(linkName, "torLink", self.bw, host, tor)
					host.addLink(hostLink)
					tor.addLink(hostLink)
					hosts.append(host)
					self.links[linkName] = hostLink
				aggrs.append(aggr)
				tors.append(tor)
		# connecting tor and aggr switches
		for i in range(self.k):
			for j in range(self.k/2):
				for l in range(self.k/2):
					name = tors[self.k/2*i+j].getID()+"+"+aggrs[self.k/2*i+l].getID()
					torLink = Link(name, "aggrLink", self.bw, tors[self.k/2*i+j], aggrs[self.k/2*i+l])
					tors[self.k/2*i+j].addLink(torLink)
					aggrs[self.k/2*i+l].addLink(torLink)
					self.links[name] = torLink
		# connecting aggr and core switches
		for i in range(self.k):
			for j in range(self.k/2):
				for l in range(self.k/2):
					name = aggrs[self.k/2*i+j].getID()+"+"+cores[j/2*j+l].getID()
					coreLink = Link(name, "coreLink", self.bw, aggrs[self.k/2*i+j], cores[j/2*j+l])
					aggrs[self.k/2*i+j].addLink(coreLink)
					cores[j/2*j+l].addLink(coreLink)
					self.links[name] = coreLink
		# populate list of devices
		for host in hosts:
			_id = host.getID()
			self.devices[_id] = host
			self.availabilityUnderHosts[_id] = (self.VMsInHost, self.bw)
		for tor in tors:
			self.devices[tor.getID()] = tor
			self.availabilityUnderRacks[_id] = (self.VMsInRack, self.bw)
		for aggr in aggrs:
			self.devices[aggr.getID()] = aggr
			self.availabilityUnderPods[_id] = (self.VMsInPod, self.bw)
		for core in cores:
			self.devices[core.getID()] = core
		self.availabilityUnderDC = (self.VMsInDC, self.bw)
		return True


	def getAllHosts(self):
		return [_device for _device in self.devices.values() if _device.getLabel() == "host"]

	def getAllTors(self):
		return [_device for _device in self.devices.values() if _device.getLabel() == "tor"]

	def getAllAggrs(self):
		return [_device for _device in self.devices.values() if _device.getLabel() == "aggr"]

	def getAllCores(self):
		return [_device for _device in self.devices.values() if _device.getLabel() == "core"]


	def failComponent(self, compID):
		try:
			comp = self.devices[compID]
		except:
			comp = self.links[compID]
		comp.setStatus(Status.FAIL)


	def recoverComponent(self, compID):
		try:
			comp = self.devices[compID]
		except:
			comp = self.links[compID]
		comp.setStatus(Status.AVAILABLE)


	def allocate(self, id, vms, bw):
		if vms < self.VMsInHost:
			for _id, _avail in self.availabilityUnderHosts.iteritems():
				if _avail[0] >= vms and _avail[1] >= bw:
					if self.alloc(self.devices[_id], vms, bw):
						return True

		if vms < self.VMsInRack:
			for _id, _avail in self.availabilityUnderRacks.iteritems():
				if _avail[0] >= vms and _avail[1] >= bw:
					if self.alloc(self.devices[_id], vms, bw):
						return True

		if vms < self.VMsInPod:
			for _id, _avail in self.availabilityUnderPods.iteritems():
				if _avail[0] >= vms and _avail[1] >= bw:
					if self.alloc(self.devices[_id], vms, bw):
						return True

		if vms < self.VMsInDC:
			availVMs = self.availabilityUnderDC[0]
			availBW = self.availabilityUnderDC[1]
			if availVMs >= vms and availBW >= bw:
				if self.alloc(self.devices[_id], vms, bw):
					return True

		return False


	def alloc(self, device, vms, bw):
		return True



	def deallocate(self, id):
		return True

