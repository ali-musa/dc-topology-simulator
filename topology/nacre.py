"""Nacre also known as mother of pearl. It is strong and resilient."""
from topology import *
import config as cfg

import globals as globals

class Nacre(Tree):
	def __init__(self):
		Tree.__init__(self, TopologyType.FATTREE)
		self.k = cfg.k_Nacre
		self.bw = cfg.bandwidthPerLink
		self.VMsInHost = cfg.VMsInHost
		
# over-loaded __str__() for print functionality
	def __str__(self):
		printString = "=========================="
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
			if(cfg.overrideDefaults):
				self.k = int(raw_input("Enter value of k: "))
			assert (self.k > 0) and (self.k % 4 == 0)
		except:
			globals.simulatorLogger.error("Invalid inputs! Please try again. Exiting...")
			return None

		globals.simulatorLogger.info("Generating " + str(self.k) + "-ary Nacre topology")
		
		#pseudo code
		#In this topoolgoy tors and aggregators are indistinguishable.  "tors" refers
		#to both tors and aggrs.
		#Please refer to /topology/nacre_jargon.png for a pictorial description of
		#primary, backup, sideA and sideB
		#create all cores.
		#for each pod in the k pods
		#	create all tors within the pod
		#	for each primary, backup tor pair
		#		create and connect hosts in strides of k/2
		#	for each sideA tor
		#		connect it with sideB tor
		#		do this for both primary and backup
		#	for each tor within the pod
		#		connect respective cores in strides of k/4

					
		# initialize components
		primaryCoresOnSideA = []
		backupCoresOnSideA = []
		primaryCoresOnSideB = []
		backupCoresOnSideB = []
		
		#create all cores
		for coreNumber in range((self.k * self.k) / 16):
			primaryCoresOnSideA.append(self.createDevice("c_A_primary" + str(coreNumber), "core"))
			backupCoresOnSideA.append(self.createDevice("c_A_backup" + str(coreNumber), "core"))
			primaryCoresOnSideB.append(self.createDevice("c_B_primary" + str(coreNumber), "core"))
			backupCoresOnSideB.append(self.createDevice("c_B_backup" + str(coreNumber), "core"))

		for podNumber in range(self.k):
			#create all tors
			primaryTorsInPodSideA = []
			backupTorsInPodSideA = []
			primaryTorsInPodSideB = []
			backupTorsInPodSideB = []
			for torNumber in range(self.k / 4):
				torA_Primary = self.createDevice("t_" + str(podNumber) + "_A_primary_" + str(torNumber),"tor")
				torA_Backup = self.createDevice("t_" + str(podNumber) + "_A_backup_" + str(torNumber),"tor")
				primaryTorsInPodSideA.append(torA_Primary)
				backupTorsInPodSideA.append(torA_Backup)
				
				torB_Primary = self.createDevice("t_" + str(podNumber) + "_B_primary_" + str(torNumber),"tor")
				torB_Backup = self.createDevice("t_" + str(podNumber) + "_B_backup_" + str(torNumber),"tor")
				primaryTorsInPodSideB.append(torB_Primary)
				backupTorsInPodSideB.append(torB_Backup)

				#create hosts and connect them
				for hostNumber in range(self.k / 2):
					hostA = self.createDevice("h_" + str(podNumber) + "_A_" + str(torNumber) + "_" + str(hostNumber),"host",True)
					hostB = self.createDevice("h_" + str(podNumber) + "_B_" + str(torNumber) + "_" + str(hostNumber),"host",True)
					self.connectDeviceAB(hostA,torA_Primary,"torLink")
					self.connectDeviceAB(hostA,torA_Backup,"torLink")
					self.connectDeviceAB(hostB,torB_Primary,"torLink")
					self.connectDeviceAB(hostB,torB_Backup,"torLink")

			#make intra pod connections
			for torA_Prim in primaryTorsInPodSideA:
				for torB_Prim in primaryTorsInPodSideB:
					self.connectDeviceAB(torA_Prim,torB_Prim,"aggrLink")
			for torA_Back in backupTorsInPodSideA:
				for torB_Back in backupTorsInPodSideB:
					self.connectDeviceAB(torA_Back,torB_Back,"aggrLink")
		
			#connect cores to tor within each pod
			torIndex = 0
			for torA_Prim in primaryTorsInPodSideA:
				for coreIndex in range(self.k / 4):
					self.connectDeviceAB(torA_Prim, primaryCoresOnSideA[coreIndex + (torIndex * self.k / 4)],"coreLink")
				torIndex+=1
			torIndex = 0
			for torB_Prim in primaryTorsInPodSideB:
				for coreIndex in range(self.k / 4):
					self.connectDeviceAB(torB_Prim, primaryCoresOnSideB[coreIndex + (torIndex * self.k / 4)],"coreLink")
				torIndex+=1
			torIndex = 0
			for torA_Back in backupTorsInPodSideA:
				for coreIndex in range(self.k / 4):
					self.connectDeviceAB(torA_Back, backupCoresOnSideA[coreIndex + (torIndex * self.k / 4)],"coreLink")
				torIndex+=1
			torIndex = 0
			for torB_Back in backupTorsInPodSideB:
				for coreIndex in range(self.k / 4):
					self.connectDeviceAB(torB_Back, backupCoresOnSideB[coreIndex + (torIndex * self.k / 4)],"coreLink")
				torIndex+=1
		globals.simulatorLogger.info(str(self.k) + "-ary Nacre topology generation successful")
		return True


	#def allocate(self, id, vms, bw):
	#	raise NotImplementedError("Subclasses should implement this!")

	def deallocate(self, id):
		raise NotImplementedError("Subclasses should implement this!")

			