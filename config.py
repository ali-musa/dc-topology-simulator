#-------------------------------------------------------------------------------
# Name:        config
# Purpose:
#-------------------------------------------------------------------------------

from base.enum import *
import time
import datetime


overrideDefaults = False #set it to True to get user input

#-----------------------------------
# Logging
#----------------------------------
ts = time.time()
currentTime = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H-%M-%S')
logLevel = "INFO"
logFilename = "./logs/simulator_"+currentTime+".log"
logEachEvent = True # set it to True to get logs for every event (failure, recovery etc.) that occurs

metricLevel = "INFO"
metricFilename = "./logs/metrics_"+currentTime+".log"


#-----------------------------------
# Simulation
#----------------------------------
simulationTime = 1*365*24*60*60 # years, days, hours, minutes, seconds
numberOfRequests = 1000

#-----------------------------------
# Topology
#----------------------------------
defaultTopology = TopologyType.NACRE
VMsInHost = 8
bandwidthPerLink = 1000 #MB
# Fat Tree
k_FatTree = 16
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
defaultTrafficType = TrafficType.FLOW
defaultTrafficCharacteristics = TrafficCharacteristics.UNIFORM_RANDOM
defaultAllocationStrategy = AllocationStrategy.RANDOM_SOURCE_DESTINATION
defaultBackupStrategy = BackupStrategy.TOR_TO_TOR
messageDelayPerHop = 0#25.0/1000000.0 #ref: DCTCP, RTT with empty queues in DCs
dataDelayPerHop =0# 25.0/1000000.0
backupReactionTime = 0

# Random source destination
numberOfBackups = 2

# Oktopus

