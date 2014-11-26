#-------------------------------------------------------------------------------
# Name:        config
# Purpose:
#-------------------------------------------------------------------------------

from base.enum import *

OverrideDefaults = False # set it to True to get user input

#-----------------------------------
# Logging
#----------------------------------
logLevel = "DEBUG"
logFilename = "simulator.log"
logEachEvent = False # set it to True to get logs for every event (failure, recovery etc.) that occurs

#-----------------------------------
# Simulation
#----------------------------------
SimulationTime = 1*365*24*60*60 # years, days, hours, minutes, seconds
NumberOfRequests = 30
AllocationStrategy = AllocationStrategy.OKTOPUS
BackupStrategy = BackupStrategy.TOR_TO_TOR

#-----------------------------------
# Topology
#----------------------------------
DefaultTopology = TopologyType.FATTREE
VMsInHost = 8
BandwidthPerLink = 1000
# Fat Tree
k_FatTree = 8
# JellyFish
k_JellyFish = 4
N_JellyFish = 20 # number of ToRs
r_JellyFish = 3 # interconnections per ToR
# Nacre
k_Nacre = 16
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