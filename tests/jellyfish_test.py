import unittest
from topology.jellyfish import *
import config as cfg
import collections

class Test_jellyfish(unittest.TestCase):
	def test_hoplength(self):
		cfg.k_JellyFish = 14 #686 server fattree => k=14
		cfg.N_JellyFish = 245 #(5/4)k^2 switches in fattree => N=245
		cfg.r_JellyFish = 11 # 686 servers divided equally across 245 racks ~=3 servers per rack => r =14-3 = 11
		jellyfish = JellyFish()
		jellyfish.generate()
		hosts = jellyfish.getHosts()
		
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
				pathlengths.append(len(jellyfish.findPath(randSource, randDest))-1)
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
		for k in range(4,10,2):
			for N in range(4,10):
				for r in range(1,min(k,N)):
					cfg.N_JellyFish = N
					cfg.k_JellyFish = k
					cfg.r_JellyFish = r
					jellyfish = JellyFish()
					print (N,k,r)
					assert(jellyfish.generate())
			
		for N in range(4,10):
			for k in range(4,100,8):
				for r in range(1,min(k,N)/2,2):
					cfg.N_JellyFish = N
					cfg.k_JellyFish = k
					cfg.r_JellyFish = r
					jellyfish = JellyFish()
					print (N,k,r)
					assert(jellyfish.generate())
	
		for k in range(4,10,2):
			for N in range(4,1250,50):
				for r in range(1,min(k,N)/2,2):
					cfg.N_JellyFish = N
					cfg.k_JellyFish = k
					cfg.r_JellyFish = r
					jellyfish = JellyFish()
					print (N,k,r)
					assert(jellyfish.generate())

		for k in range(10,100,16):
			for N in range(10,1250,200):
				for r in range(1,min(k,N)/2,9):
					cfg.N_JellyFish = N
					cfg.k_JellyFish = k
					cfg.r_JellyFish = r
					jellyfish = JellyFish()
					print (N,k,r)
					assert(jellyfish.generate())
		return True

if __name__ == '__main__':
	unittest.main()

