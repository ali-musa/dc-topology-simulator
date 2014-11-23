import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import unittest
from topology.nacre import *
import config as cfg
import collections
import random

# *** START OF LOGGING CONFIGURATIONS ***
import logging
logging.basicConfig(format='%(levelname)s : %(message)s', level=logging.INFO)
# *** END OF LOGGING CONFIGURATIONS ***
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

if __name__ == '__main__':
	unittest.main()