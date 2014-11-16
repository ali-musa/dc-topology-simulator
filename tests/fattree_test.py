import unittest
from topology.fattree import *
import config as cfg
import collections

class Test_fattree(unittest.TestCase):
	def test_simplePath(self):
		cfg.k_FatTree = 4
		fattree = FatTree()
		fattree.generate()
		fattree.printTopo()
		source = 'h_1_1_1'
		dest = 'h_3_2_2'
		possibleECMPs = [['h_1_1_1', 't_1_1', 'a_1_1', 'c_1', 'a_3_1', 't_3_2', 'h_3_2_2'],
				   ['h_1_1_1', 't_1_1', 'a_1_1', 'c_2', 'a_3_1', 't_3_2', 'h_3_2_2'],
				   ['h_1_1_1', 't_1_1', 'a_1_2', 'c_3', 'a_3_2', 't_3_2', 'h_3_2_2'],
				   ['h_1_1_1', 't_1_1', 'a_1_2', 'c_4', 'a_3_2', 't_3_2', 'h_3_2_2']]
		pathComponents = fattree.findPath(source,dest)
		path = []
		for component in pathComponents:
			path.append(component.id)
		assert path in possibleECMPs
		print("FatTree hop length: %.2f " % (len(path)-1))
		return True


	def test_hoplength(self):
		cfg.k_FatTree= 14 #686 server fattree => k=14
		fattree = FatTree()
		fattree.generate()
		hosts = fattree.getHosts()
		
		trials = 10 #10 trials as given
		iterations =10
		distribution=dict()
		for iteration in range(iterations):
			pathlengths = []
			for trial in range(trials):
				randSource = random.choice(hosts.keys()) #pick a random source
				randDest = random.choice(hosts.keys()) #pick a random destination
				while(randSource==randDest):
					randDest = random.choice(hosts.keys())
				pathlengths.append(len(fattree.findPath(randSource, randDest))-1)
			pathlengths.sort()
			frequency=collections.Counter(pathlengths)
			for key in frequency.keys():
				if key in distribution.keys():
					distribution[key]+=frequency[key]
				else:
					distribution[key]=frequency[key]
		
		print("Distribution")			
		print(distribution.keys())
		print([float(x) / (trials*iterations) for x in distribution.values()])
		return True
	
	def test_various_inputs(self):
		for k in range(4,100,2):
			cfg.k_FatTree = k
			fattree = FatTree()
			print (k)
			assert(fattree.generate())
		return True

if __name__ == '__main__':
	unittest.main()
