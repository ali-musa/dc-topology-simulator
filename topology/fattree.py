from topology import *
import config as cfg
import logging

class FatTree(Tree):
	def __init__(self):
		Tree.__init__(self, TopologyType.FATTREE)
		self.k = cfg.k_FatTree
		self.bw = cfg.BandwidthPerLink
		self.VMsInHost = cfg.VMsInHost
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
			# *** TAKE INPUT FROM USER. ***
			if(cfg.OverrideDefaults):
				self.k = int(raw_input("Enter value of k: "))
			assert (self.k > 0) and (self.k%2 == 0)
		except:
			logging.error("Invalid inputs! Please try again. Exiting...")
			return None

		logging.info("Generating " + str(self.k) + "-ary FatTree topology")
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
			core = Device(coreName, "core")
			cores.append(core)
		# add pods with k/2 aggrs and k/2 tors, with k/2 hosts per tor
		for pod in range(self.k):
			for sw in range(self.k/2):
				aggrName = "a_" + str(pod+1) + "_" + str(sw+1)
				torName = "t_" + str(pod+1) + "_" + str(sw+1)
				aggr = Device(aggrName, "aggr")
				tor = Device(torName, "tor")
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
		for podNumber in range(self.k):
			for aggregatorNumberInPod in range(self.k/2):
				for coreNumber in range(self.k/2):
					name = aggrs[podNumber*(self.k/2)+aggregatorNumberInPod].getID()+"+"+cores[aggregatorNumberInPod*(self.k/2)+coreNumber].getID()
					coreLink = Link(name, "coreLink", self.bw, aggrs[podNumber*(self.k/2)+aggregatorNumberInPod], cores[aggregatorNumberInPod*(self.k/2)+coreNumber])
					aggrs[podNumber*(self.k/2)+aggregatorNumberInPod].addLink(coreLink)
					cores[aggregatorNumberInPod*(self.k/2)+coreNumber].addLink(coreLink)
					self.links[name] = coreLink			
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


	
	def findPath(self, _id, _label, _time, _active, start, end, _bw):
		_start = self.devices[start] # start node
		_end = self.devices[end] # end node

		startSW = _start.getLink().getOtherDevice(_start)
		endSW = _end.getLink().getOtherDevice(_end)
		startPod = _start.getID().split("_")[1]
		endPod = _end.getID().split("_")[1]

		if startSW == endSW:
			pass
		elif startPod == endPod:
			paths = self.getIntraPodPaths(_start, _end, _bw)
		else:
			paths = self.getInterPodPaths(_start, _end, _bw)

		primaryPath = random.choice(list(paths))
		ind = paths.index(primaryPath)
		del paths[ind]

		flow = Flow(_id, _label, _time, _active, _bw, _start, _end)
		flow.addPath(primaryPath)
		return flow

	def getIntraPodPaths(self, _start, _end, _bw):
		paths = []
		startSW = _start.getLink().getOtherDevice(_start)
		endSW = _end.getLink().getOtherDevice(_end)

		for aggrLink in startSW.getAllLinks():
			aggrSW = aggrLink.getOtherDevice(startSW)
			if not aggrSW.getStatus() == Status.AVAILABLE:
				continue
			aggrBW = aggrLink.getAvailableBW(startSW)

			if aggrSW.getID().split("_")[0] == "a" and aggrBW >= _bw:
				for torLink in aggrSW.getAllLinks():
					torSW = torLink.getOtherDevice(aggrSW)
					if torSW.getStatus() is not Status.AVAILABLE:
						continue
					torBW = torLink.getAvailableBW(aggrSW)

					if torSW == endSW and torSW.getID().split("_")[0] == "t" and torBW >= _bw:
						path = Path()
						path.append(_start)
						path.append(_start.getLink())
						path.append(startSW)
						path.append(aggrLink)
						path.append(aggrSW)
						path.append(torLink)
						path.append(endSW)
						path.append(_end.getLink())
						path.append(_end)
						paths.append( path )
		return paths

	def getInterPodPaths(self, _start, _end, _bw):
		paths = []
		startSW = _start.getLink().getOtherDevice(_start)
		startPod = _start.getID().split("_")[1]
		endSW = _end.getLink().getOtherDevice(_end)
		endPod = _end.getID().split("_")[1]

		for aggrLink in startSW.getAllLinks():
			aggrSW = aggrLink.getOtherDevice(startSW)
			if not aggrSW.getStatus() == Status.AVAILABLE:
				continue
			aggrBW = aggrLink.getAvailableBW(startSW)

			if aggrSW.getID().split("_")[0] == "a" and aggrBW >= _bw:
				for coreLink in aggrSW.getAllLinks():
					coreSW = coreLink.getOtherDevice(aggrSW)
					if coreSW.getStatus() is not Status.AVAILABLE:
						continue
					coreBW = coreLink.getAvailableBW(aggrSW)

					if coreSW.getID().split("_")[0] == "c" and coreBW >= _bw:
						for aggLink in coreSW.getAllLinks():
							aggSW = aggLink.getOtherDevice(coreSW)
							if aggSW.getStatus() is not Status.AVAILABLE:
								continue
							aggBW = aggLink.getAvailableBW(coreSW)

							if aggSW.getID().split("_")[1] == endPod and aggSW.getID().split("_")[0] == "a" and aggBW >= _bw:
								for torLink in aggSW.getAllLinks():
									torSW = torLink.getOtherDevice(aggSW)
									if torSW.getStatus() is not Status.AVAILABLE:
										continue
									torBW = torLink.getAvailableBW(aggSW)

									if torSW == endSW and torSW.getID().split("_")[0] == "t" and torBW >= _bw:
										path = Path()
										path.append(_start)
										path.append(_start.getLink())
										path.append(startSW)
										path.append(aggrLink)
										path.append(aggrSW)
										path.append(coreLink)
										path.append(coreSW)
										path.append(aggLink)
										path.append(aggSW)
										path.append(torLink)
										path.append(endSW)
										path.append(_end.getLink())
										path.append(_end)
										paths.append( path )
		return paths


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
				# need to pick the device in this case
				# if self.alloc(self.devices[_id], vms, bw):
					# return True
				return True

		return False


	# def alloc(self, device, vms, bw):
	# 	return True


	def deallocate(self, id):
		return True

	
	# *** OKTOPUS STARTS HERE ***
	def getDownLinks(self, switch):
		downLinks = []
		
		if switch.getLabel() == "tor":
			for link in switch.getAllLinks():
				if link.getOtherDevice(switch).getLabel() == "host":
					downLinks.append(link)

		if switch.getLabel() == "aggr":
			for link in switch.getAllLinks():
				if link.getOtherDevice(switch).getLabel() == "tor":
					downLinks.append(link)

		if switch.getLabel() == "core":
			for link in switch.getAllLinks():
				if link.getOtherDevice(switch).getLabel() == "aggr":
					downLinks.append(link)

		return downLinks

	def computeMx(self, link, switch, bw):
		# checks the number of VMs that can be placed in a host, that also meet the BW requirements
		assert switch.getLabel() == "tor"
		residualBW = link.getMinBW()
		cap = residualBW/bw
		host = link.getOtherDevice(switch)
		hostVM = len(host.getAvailableVMs()) # available VMs in host
		canAllocate = min(cap, hostVM)
		return canAllocate

	def vmCount(self, device, bw):
		# counts the number of VMs under device that meet bandwidth requirement
		count = 0
		if device.getLabel() == "host":
			count = len(device.getAvailableVMs())
			return count
		if device.getLabel() == "tor":
			for link in self.getDownLinks(device):
				count = count + self.computeMx(link, device, bw)
			return count
		if device.getLabel() == "aggr":
			for link in self.getDownLinks(device):
				tor = link.getOtherDevice(device)
				count = count + self.vmCount(tor, bw)
			return count
		if device.getLabel() == "core":
			for link in self.getDownLinks(device):
				aggr = link.getOtherDevice(device)
				count = count + self.vmCount(aggr, bw)
			return count

	def oktopus(self, numVMs, bw, tenant):

		hosts = self.getAllHosts()
		for host in hosts:
			Mv = self.vmCount(host, bw)
			if numVMs <= Mv:
				self.alloc(host, numVMs, bw, tenant)
				logging.info("Allocating under Host: \n")
				logging.info(host)
				return True
		
		tors = self.getAllTors()
		for tor in tors:
			Mv = self.vmCount(tor, bw)
			if numVMs <= Mv:
				self.alloc(tor, numVMs, bw, tenant)
				logging.info("Allocating under Tor: \n")
				logging.info(tor)
				return True
		
		aggrs = self.getAllAggrs()
		for aggr in aggrs:
			Mv = self.vmCount(aggr, bw)
			if numVMs <= Mv:
				self.alloc(aggr, numVMs, bw, tenant)
				logging.info("Allocating under Aggr: \n")
				logging.info(aggr)
				return True

		cores = self.getAllCores()
		for core in cores:
			Mv = self.vmCount(core, bw)
			if numVMs<= Mv:
				self.alloc(core, numVMs, bw, tenant)
				logging.info("Allocating under Core: \n")
				logging.info(core)
				return True
		
		logging.warning("Could not be allocated!")
		return False

	def alloc(self, device, numVMs, bw, tenant):
		if device.getLabel() == "host":
			link = device.getLink()
			residualBW = link.getMinBW()
			cap = residualBW/bw
			hostVM = len(device.getAvailableVMs()) # available VMs in host
			canAllocate = min(cap, hostVM)
			availableVMs = device.getAvailableVMs()
			for i in range(canAllocate):
				availableVMs[i].setStatus(Status.IN_USE)
				tenant.addVM(availableVMs[i])
			tenant.addHost(device, canAllocate)
			logging.info(str(canAllocate) + " VMs placed under the following host: \n")
			logging.info(device)
			return canAllocate
		else:
			count = 0
			allocatedOnEachLink = []
			for link in self.getDownLinks(device):
				otherDevice = link.getOtherDevice(device)
				Mx = self.vmCount(otherDevice, bw)
				allocated = self.alloc(otherDevice, min(Mx, numVMs-count), bw, tenant)
				allocatedOnEachLink.append(allocated)
				count = count + allocated
			# takes the minimum of what was allocated on left and right of the switch
			# and reserves that much bandwidth on each link 
			bwOnEachLink = min(allocatedOnEachLink)*bw
			for link in self.getDownLinks(device):
				link.reserveBW_AB(bwOnEachLink)
				link.reserveBW_BA(bwOnEachLink)
				tenant.addLink(link, bwOnEachLink)
			return count