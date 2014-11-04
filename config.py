#-------------------------------------------------------------------------------
# Name:        config
# Purpose:
#-------------------------------------------------------------------------------

from base.enum import *


#-----------------------------------
# Simulation
#----------------------------------
SimulationTime = 1*365*24*60*60 # years, days, hours, minutes, seconds
NumberOfRequests = 10

#-----------------------------------
# Topology
#----------------------------------
DefaultTopology = TopologyType.FATTREE
VMsInHost = 8
BandwidthPerLink = 1000
# Fat Tree
k = 4

#-----------------------------------
# Failures
#-----------------------------------
DefaultFailureModel =  Failure.PHILLIPA
# Phillipa
ToRResilience = 0.039
AggregatorResilience = 0.07
CoreResilience = 0.02