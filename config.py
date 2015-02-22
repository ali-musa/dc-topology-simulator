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
logLevel = "DEBUG"
logFilename = "./logs/simulator_"+currentTime+".log"
logEachEvent = False # set it to True to get logs for every event (failure, recovery etc.) that occurs

metricLevel = "INFO"
metricFilename = "./logs/metrics_"+currentTime+".log"


#-----------------------------------
# Simulation
#-----------------------------------
simulationTime = 1*365*24*60*60 # years, days, hours, minutes, seconds
numberOfRequests = 500

#-----------------------------------
# Topology
#-----------------------------------
defaultTopology = TopologyType.FATTREE
VMsInHost = 4
bandwidthPerLink = 1000 #Megabits per second
# Fat Tree
k_FatTree = 24
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
# torResilience = 0.039
# aggregatorResilience = 0.07
# coreResilience = 0.02
torResilience = 0 # no failures
aggregatorResilience = 0 # no failures
coreResilience = 0 # no failures

#-----------------------------------
# Reservation
#-----------------------------------
defaultTrafficType = TrafficType.TENANT
defaultTrafficCharacteristics = TrafficCharacteristics.EXPONENTIAL
defaultAllocationStrategy = AllocationStrategy.OKTOPUS
defaultBackupStrategy = BackupStrategy.NONE
messageDelayPerHop = 25.0/1000000.0 #ref: DCTCP, RTT with empty queues in DCs
dataDelayPerHop = 25.0/1000000.0
backupReactionTime = 0
stopAfterRejects = -1 #stop accepting any more arrivals after X rejects (-1 dont stop)

meanExpoVMs = 49.0 # the mean of tenant requests (VMs) for exponential arrival
meanExpoBW = 100.0 # the mean of tenant requests (BW) for exponential arrival

# Random source destination
numberOfBackups = 0

# Oktopus
