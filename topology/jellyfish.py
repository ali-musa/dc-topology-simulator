from topology import *

class JellyFish(NonTree):
	def __init__(self):
		NonTree.__init__(self, TopologyType.JELLYFISH)
		self.N = 0
		self.k = 0
		self.r = 0
		self.numServers = 0
		self.s = 0

	def generate(self):
		try:
			self.N = int(raw_input("Enter value of N: "))
			assert self.N > 0
			self.k = int(raw_input("Enter value of k: "))
			assert self.k > 1
			self.r = int(raw_input("Enter value of r: "))
			assert self.r > 0
			self.numServers = self.N*(self.k-self.r)
			assert self.N >= self.numServers
			self.s = int(raw_input("Enter value of s: "))
			assert self.s > 0
		except:
			print "Invalid inputs! Please try again. Exiting..."
			return None

		print "Generating RRG(" + str(self.N) + "," + str(self.k) + "," + str(self.r) + ") Jellyfish topology"
		# initialize lists
		servers = []
		switches = []
		openPorts = []
		topoLinks = []
		# add the servers
		for i in range(self.numServers):
			hostName = "h_" + str(i+1)
			host = Device(hostName, "host", True)
			servers.append(host)
		# add the switches
		for i in range(self.N):
			switchName = "tor_" + str(i+1)
			switch = Device(switchName, "tor", False)
			switches.append(switch)
			openPorts.append(self.k)
		# connect each server with a switch
		for i in range(self.numServers):
			hostLink = Link(servers[i].getID()+"+"+switches[i].getID(), "hostLink", 1000, servers[i], switches[i])
			servers[i].addLink(hostLink)
			switches[i].addLink(hostLink)
			topoLinks.append(hostLink)
			openPorts[i] -= 1
		# manage the potential links, fully populate the set before creating
		switchesLeft = self.N
		consecFails = 0

		while switchesLeft > 1 and consecFails < 10:
			s1 = rangrange(self.N)
			while openPorts[s1] == 0:
				s1 = rangrange(self.N)
			s2 = rangrange(self.N)
			while openPorts[s2] == 0 or s1 == s2:
				s2 = rangrange(self.N)

			name1 = switches[s1].getID()
			name2 = switches[s2].getID()
			torLink1 = Link(name1+"+"+name2, "torLink", 1000, switches[s1], switches[s2])
			torLink2 = Link(name2+"+"+name1, "torLink", 1000, switches[s2], switches[s1])
			if torLink1 in topoLinks or torLink2 in topoLinks:
				consecFails += 1
			else:
				consecFails = 0
				switches[s1].addLink(torLink1)
				switches[s2].addLink(torLink1)
				topoLinks.append(torLink1)
				openPorts[s1] -= 1
				openPorts[s2] -= 1
				if openPorts[s1] == 0:
					switchesLeft -= 1
				if openPorts[s2] == 0:
					switchesLeft -= 1
		if switchesLeft > 0:
			for i in range(self.N):
				while openPorts[i] > 1:
					while True:
						# incremental expansion
						rLink = random.choice(list(topoLinks))
						index1 = -1
						index2 = -2
						for i in range(N):
							if switches[i] == rLink.getDownSwitch():
								index1 = i
							if switches[i] == rLink.getUpSwitch():
								index2 = i
						name11 = swithes[i].getID()+"+"+switches[index1].getID()
						name12 = swithes[index1].getID()+"+"+switches[i].getID()
						torLink11 = Link(name11, "torLink", 1000, switches[i], switches[index1])
						torLink12 = Link(name12, "torLink", 1000, switches[index1], switches[i])
						if torLink11 in topoLinks or torLink12 in topoLinks:
							continue
						name21 = swithes[i].getID()+"+"+switches[index2].getID()
						name22 = swithes[index2].getID()+"+"+switches[i].getID()
						torLink21 = Link(name21, "torLink", 1000, switches[i], switches[index2])
						torLink22 = Link(name22, "torLink", 1000, switches[index2], switches[i])
						if torLink21 in topoLinks or torLink22 in topoLinks:
							continue
						# add new links
						switches[i].addLink(torLink11)
						switches[index1].addLink(torLink11)
						switches[i].addLink(torLink21)
						switches[index2].addLink(torLink21)
						# remove links
						index1 = -1
						index2 = -2
						for i in range(self.N):
							if switches[i] == rLink.getDevice_B():
								index1 = i
							if switches[i] == rLink.getDevice_A():
								index2 = i
						switches[index1].removeLink(rLink)
						switches[index2].removeLink(rLink)
						topoLinks.remove(rLink)

						openPorts[i] -= 2
						break
		# populate list of devices
		for server in servers:
			self.devices[server.getID()] = server
		for switch in switches:
			self.devices[switch.getID()] = switch
		# populate list of links
		for link in topoLinks:
			self.links[link.getID()] = link
		return True

	def allocate(self, id, vms, bw):
		return True

	def deallocate(self, id):
		return True
