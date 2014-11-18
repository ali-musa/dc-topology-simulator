#-------------------------------------------------------------------------------
# Name:        config
# Purpose:
#-------------------------------------------------------------------------------

from base.enum import *

OverrideDefaults = False #set it to true to get user input

#-----------------------------------
# Logging
#----------------------------------
logLevel = "DEBUG"
logFilename = "simulator.log"

#-----------------------------------
# Simulation
#----------------------------------
SimulationTime = 1*365*24*60*60 # years, days, hours, minutes, seconds
NumberOfRequests = 0

#-----------------------------------
# Topology
#----------------------------------
DefaultTopology = TopologyType.FATTREE
VMsInHost = 8
BandwidthPerLink = 100
# Fat Tree
k_FatTree = 4
# JellyFish
k_JellyFish = 4
N_JellyFish = 20 # number of ToRs
r_JellyFish = 3 # interconnections per ToR
# Custom
customTopoFilename = "custom-topology.txt"

#-----------------------------------
# Failures
#-----------------------------------
DefaultFailureModel =  FailureType.PHILLIPA
# Phillipa
ToRResilience = 0.039
AggregatorResilience = 0.07
CoreResilience = 0.02