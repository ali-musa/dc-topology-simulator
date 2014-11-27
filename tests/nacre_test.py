import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import unittest
from topology.nacre import *
import collections
import random
from utils.visualization import *
from init import *

class Test_nacre_test(unittest.TestCase):
	def test_hoplength(self):
		cfg.k_Nacre = 16
		nacre = Nacre()
		nacre.generate()
		hosts = nacre.getHosts()
		
		trials = 50
		iterations = 10
		distribution = dict()
		for iteration in range(iterations):
			pathlengths = []
			for trial in range(trials):
				randSource = random.choice(hosts.keys()) #pick a random source
				randDest = random.choice(hosts.keys()) #pick a random destination
				while(randSource == randDest):
					randDest = random.choice(hosts.keys())
				pathlengths.append(len(nacre.findPath(randSource, randDest)) - 1)
			pathlengths.sort()
			frequency = collections.Counter(pathlengths)
			for key in frequency.keys():
				if key in distribution.keys():
					distribution[key]+=frequency[key]
				else:
					distribution[key] = frequency[key]
		
		print("Distribution")			
		print(distribution.keys())
		print([float(x) / (trials * iterations) for x in distribution.values()])
		return True

	def test_various_inputs(self):
		for k in range(4,100,4):
			cfg.k_Nacre= k
			nacre = Nacre()
			assert(nacre.generate())
		return True

	def test_simple_flow(self):
		nacre = Nacre()
		assert(nacre.generate())
		globals.simulatorLogger.info("Nacre generated")
		assert(nacre.allocate(Flow(1,10,'h_1_A_1_1','h_3_B_2_1',100)))
		globals.metricLogger.info("Simple flow allocated")
		return True
		
	def test_disjointPath(self):
		cfg.k_Nacre= 20
		cfg.defaultBackupStrategy= BackupStrategy.TOR_TO_TOR
		nacre = Nacre()
		nacre.generate()
		source = 'h_1_A_1_1'
		dest = 'h_3_B_2_1'
		paths = []
		while True:
			path = nacre.findDisjointPath(source,dest,0,paths)
			if path is not None:
				paths.append(path)
				globals.simulatorLogger.info(path.__str__())
			else:
				break
		globals.simulatorLogger.info("Total disjoint paths found %s" % len(paths))
		return True
		


if __name__ == '__main__':
	unittest.main()
