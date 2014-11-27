#-------------------------------------------------------------------------------
# Name:        config
# Purpose:
#-------------------------------------------------------------------------------

from base.enum import *

overrideDefaults = False #set it to True to get user input

#-----------------------------------
# Logging
#----------------------------------
logLevel = "INFO"
logFilename = "simulator.log"
logEachEvent = True # set it to True to get logs for every event (failure, recovery etc.) that occurs

metricLevel = "INFO"
metricFilename = "metrics.log"


#-----------------------------------
# Simulation
#----------------------------------
simulationTime = 1*365*24*60*60 # years, days, hours, minutes, seconds
numberOfRequests = 0

#-----------------------------------
# Topology
#----------------------------------
defaultTopology = TopologyType.FATTREE
VMsInHost = 8
bandwidthPerLink = 100
# Fat Tree
k_FatTree = 4
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
defaultFailureModel =  FailureType.PHILLIPA
# Phillipa
torResilience = 0.039
aggregatorResilience = 0.07
coreResilience = 0.02

#-----------------------------------
# Reservation
#-----------------------------------
defaultAllocationStrategy = AllocationStrategy.FLOW
defaultBackupStrategy = BackupStrategy.TOR_TO_TOR
# Flow
numberOfBackups = 2
# Oktopus
numberOfRequests = 30
