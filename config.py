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
#-----------------------------------
ts = time.time()
currentTime = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H-%M-%S')
logLevel = "INFO"
logFilename = "./logs/simulator_"+currentTime+".log"
logEachEvent = False # set it to True to get logs for every event (failure, recovery etc.) that occurs

metricLevel = "INFO"
metricFilename = "./logs/metrics_"+currentTime+".log"


#-----------------------------------
# Simulation
#-----------------------------------
simulationTime = 1*365*24*60*60 # years, days, hours, minutes, seconds
numberOfRequests = 100

#-----------------------------------
# Topology
#-----------------------------------
defaultTopology = TopologyType.NACRE
bandwidthPerLink = 1000 #Megabits per second
messageDelayPerHop = 25.0/1000000.0 #ref: DCTCP, RTT with empty queues in DCs
dataDelayPerHop = 25.0/1000000.0
VMsInHost = 8
# Fat Tree
k_FatTree = 24
# JellyFish
k_JellyFish = 24
N_JellyFish = 720 # number of ToRs
r_JellyFish = 19 # interconnections per ToR 3456
# Nacre
k_Nacre = 24
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
backupReactionTime = 0
stopAfterRejects = -1 #stop accepting any more arrivals after X rejects (-1 dont stop)
stopAfterAccepts = -1 #stop accepting any more arrivals after X accepts (-1 dont stop)

# Random source destination
numberOfBackups = 0

# Oktopus

