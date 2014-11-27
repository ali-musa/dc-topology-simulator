from topology import *
import config as cfg
import random
import globals as globals

class JellyFish(NonTree):
	def __init__(self):
		NonTree.__init__(self, TopologyType.JELLYFISH)
		self.N = cfg.N_JellyFish
		self.k = cfg.k_JellyFish
		self.r = cfg.r_JellyFish
	
	def generate(self):
		try:
			if(cfg.overrideDefaults):
				self.N = int(raw_input("Enter value of N: "))
				self.k = int(raw_input("Enter value of k: "))
				self.r = int(raw_input("Enter value of r: "))
			assert self.k>1
			assert 0<self.r<min(self.k,self.N)
			self.numServers = self.N*(self.k-self.r)
			assert self.N>=4 
		except:
			globals.simulatorLogger.error("Invalid inputs! Please try again. Exiting...")
			return None

		globals.simulatorLogger.info("Generating RRG(" + str(self.N) + "," + str(self.k) + "," + str(self.r) + ") Jellyfish topology")

		#following the author's algorithm

		# pesudocode:
		#	while open ports > 0
		#		select two different random switches
		#		connect if not neighbours and close connected ports
		#		repeat until open 100,000 iterations or only one switch left with open ports or two neighbouring switches left with open ports
		#	
		#	failover to incremental expansion
		#	iterate over all switches with open ports >=2
		#		while open ports for a switch >=2
		#			choose a random link as long as it is not connected to the neighbours of the switch in question
		#				delete the chosen link
		#				connect the switch with the freed ports
		#				close ports
		#
		#	connecting endhosts
		#		for each switch connect k-r endhosts one by one

		
		# Init components
		switches = []
		openPorts = [] #these map directly onto the switches
		openIndices = []
		links=[]
		for switchIndex in range(self.N):
			switches.append(Device("switch"+str(switchIndex), "tor"))
			openPorts.append(self.r)

		#randomly select swtiches and connect them if they are not already connected
		iterations = 0
		while sum(openPorts) > 0:
			iterations+=1
			if iterations>=100000:
				break
			openIndices = [index for index,value in enumerate(openPorts) if value != 0]
			if(len(openIndices)<=2):
				if(len(openIndices)==1):
					break
				if(switches[openIndices[0]] in switches[openIndices[1]].getNeighbours()):
					break
			sw1Index=random.choice(openIndices)
			sw2Index=random.choice(openIndices)
			if((sw1Index==sw2Index) or (switches[sw2Index] in switches[sw1Index].getNeighbours())):
				continue
			sw1=switches[sw1Index]
			sw2=switches[sw2Index]
			link = Link(str(sw1.getID())+"_"+str(sw2.getID()),"jellyFishLink",cfg.bandwidthPerLink,sw1,sw2)
			links.append(link)
			sw1.addLink(link)
			sw2.addLink(link)
			openPorts[sw1Index]-=1
			openPorts[sw2Index]-=1
			
		globals.simulatorLogger.debug("Starting jellyfish incremental expansion")	
		#failover to incremental expansion
		for index in openIndices:
			while openPorts[index]>=2:
				link = random.choice(links)
				switchA = link.getDevice_A()
				switchB = link.getDevice_B()
				sw = switches[index]
				if ((switchA not in sw.getNeighbours()) and (switchB not in sw.getNeighbours())):
					links.remove(link)
					switchA.removeLink(link)
					switchB.removeLink(link)
					del link
					newLinkA = Link(str(switchA.getID())+"_"+str(sw.getID()),"jellyFishLink",cfg.bandwidthPerLink,switchA,sw) 
					newLinkB = Link(str(switchB.getID())+"_"+str(sw.getID()),"jellyFishLink",cfg.bandwidthPerLink,switchB,sw)
					switchA.addLink(newLinkA)
					switchB.addLink(newLinkB)
					sw.addLink(newLinkA)
					sw.addLink(newLinkB)
					links.append(newLinkA)
					links.append(newLinkB)
					openPorts[index]-=2

		#connect endhosts with all the switch one by one
		hosts=[]
		numberOfHosts = self.N*(self.k-self.r)
		for hostIndex in range(numberOfHosts):
			host = Device("host"+str(hostIndex),"host",True)
			sw=switches[hostIndex%self.N]
			link = Link(str(sw.getID())+"_"+str(host.getID()),"jellyFishLink",cfg.bandwidthPerLink,sw,host)
			links.append(link)
			sw.addLink(link)
			host.addLink(link)
			self.devices[host.getID()] = host

		# populate list of devices
		for switch in switches:
			self.devices[switch.getID()] = switch
		# populate list of links
		for link in links:
			self.links[link.getID()] = link
		globals.simulatorLogger.info("RRG(" + str(self.N) + "," + str(self.k) + "," + str(self.r) + ") Jellyfish topology generation successful")
		return True

	def allocate(self, id, vms, bw):
		return True

	def deallocate(self, id):
		return True
