import unittest
from topology.fattree import *
import config as cfg

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

if __name__ == '__main__':
	unittest.main()
