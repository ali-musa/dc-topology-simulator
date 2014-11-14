import unittest
from topology.jellyfish import *
import config as cfg

class Test_jellyfish(unittest.TestCase):
	def test_hoplength(self):
		cfg.k_JellyFish = 14 #686 server fattree => k=14
		cfg.N_JellyFish = 245 #(5/4)k^2 switches in fattree => N=245
		cfg.r_JellyFish = 11 # 686 servers divided equally across 245 racks ~=3 => r =14-3 = 11
		jellyfish = JellyFish()
		jellyfish.generate()
		jellyfish.printTopo()
		hosts = jellyfish.getHosts()
		iterations = 10 #10 trials as given
		pathlengths = []
		for iteration in range(iterations):
			randSource = random.choice(hosts.keys()) #pick a random source
			randDest = random.choice(hosts.keys()) #pick a random destination
			while(randSource==randDest):
				randDest = random.choice(hosts.keys())
			pathlengths.append(len(jellyfish.findPath(randSource, randDest))-1)
		avgHopLength = float(sum(pathlengths))/iterations
		print("JellyFish average path length: %.2f " % (avgHopLength))



if __name__ == '__main__':
	unittest.main()
