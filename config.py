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
simulationTime = 3*365*24*60*60 # years, days, hours, minutes, seconds
numberOfRequests = 10

#-----------------------------------
# Topology
#-----------------------------------
defaultTopology = TopologyType.FATTREE
VMsInHost = 8
bandwidthPerLink = 1000 #Megabits per second
# Fat Tree
k_FatTree = 16
# JellyFish
k_JellyFish = 16
N_JellyFish = 320 # number of ToRs
r_JellyFish = 12 # interconnections per ToR
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
defaultTrafficType = TrafficType.TENANT
defaultTrafficCharacteristics = TrafficCharacteristics.UNIFORM_RANDOM
defaultAllocationStrategy = AllocationStrategy.OKTOPUS
defaultBackupStrategy = BackupStrategy.TOR_TO_TOR
messageDelayPerHop = 25.0/1000000.0 #ref: DCTCP, RTT with empty queues in DCs
dataDelayPerHop = 25.0/1000000.0
backupReactionTime = 0
stopAfterRejects = -1 #stop accepting any more arrivals after X rejects (-1 dont stop)

# Random source destination
numberOfBackups = 2

# Oktopus
