from __future__ import absolute_import
import globals as globals
from base.event import *
from base.enum import *
from utils.helper import *
from topology.topology import *
from topology.fattree import *
from topology.jellyfish import *
from topology.nacre import *
from failure.failure import *
from traffic.tenant import *
import config as cfg
import random
import time
import logging
import gc
from initializer import *
import argparse

gc.enable() #enable automatic garbage collection

random.seed()

## ***START Command line arguments***
#parser = argparse.ArgumentParser(description='Network Simulator')

#parser.add_argument('-useconfig', type=bool, default=False, 
#					help='a boolean, True overwrites defaults and loads all configurations from config.py (default: False)')
#parser.add_argument('-backups', type=int, default=0, help='an integer for the number of backups (default: 0)')
#parser.add_argument('-topology', default='FATTREE', help='an all-caps string for the topology to use. (default: FATTREE)')
#parser.add_argument('-requests', type=int, default='100', help='an integer for the number of requests to spawn. (default: 100)')
#parser.add_argument('-stopafterrejects', type=int, default='-1', help='an integer for the number of requests to reject before stopping. (default: -1 {does not stop})')
#parser.add_argument('-stopafteraccepts', type=int, default='-1', help='an integer for the number of requests to accept before stopping. (default: -1 {does not stop})')
#parser.add_argument('-backupstrategy', default='FLEXIBLE_REPLICA', help='an all-caps string for the backup strategy to use. (default: TOR_TO_TOR)')

#args = parser.parse_args()
#if(not args.useconfig):
#	cfg.numberOfBackups=args.backups
#	cfg.numberOfRequests=args.requests
#	cfg.stopAfterRejects=args.stopafterrejects
#	cfg.stopAfterAccepts=args.stopafteraccepts
#	#TODO: need some better way to do the following
#	if('FATTREE'==args.topology):
#		cfg.defaultTopology=TopologyType.FATTREE
#	elif('JELLYFISH'==args.topology):
#		cfg.defaultTopology=TopologyType.JELLYFISH
#	elif('NACRE'==args.topology):
#		cfg.defaultTopology=TopologyType.NACRE
#	elif('CUSTOM'==args.topology):
#		cfg.defaultTopology=TopologyType.CUSTOM
#	else:
#		raise EnvironmentError("Invalid input arguments")

	
#	if('TOR_TO_TOR'==args.backupstrategy):
#		cfg.defaultBackupStrategy=BackupStrategy.TOR_TO_TOR
#	elif('END_TO_END'==args.backupstrategy):
#		cfg.defaultBackupStrategy=BackupStrategy.END_TO_END
#	elif('FLEXIBLE_REPLICA'==args.backupstrategy):
#		cfg.defaultBackupStrategy=BackupStrategy.FLEXIBLE_REPLICA
#	elif('NONE'==args.backupstrategy):
#		cfg.defaultBackupStrategy=BackupStrategy.NONE
#	else:
#		raise EnvironmentError("Invalid input arguments")

# ***END Command line arguments***
	

# *** START OF LOGGING CONFIGURATIONS ***
def setup_logger(logger_name, log_file, level=logging.INFO):
	l = logging.getLogger(logger_name)

	# NOTE: append "%(asctime)s" to format attribute below for showing time of log
	# message
	# NOTE: append "%(levelname)s" to format attribute below for showing log level
	# name
	# NOTE: filemode='w' makes a new file every time.  remove this parameter to
	# continue writing to same file every time.
	formatter = logging.Formatter('%(levelname)s : %(message)s')
	fileHandler = logging.FileHandler(log_file, mode='w')
	fileHandler.setFormatter(formatter)
	streamHandler = logging.StreamHandler()
	streamHandler.setFormatter(formatter)

	l.setLevel(level)
	l.addHandler(fileHandler)

logLevel = getattr(logging, cfg.logLevel.upper(), None)
if not isinstance(logLevel, int):
	raise ValueError('Invalid log level: %s' % logLevel)

metricLevel = getattr(logging, cfg.metricLevel.upper(), None)
if not isinstance(metricLevel, int):
	raise ValueError('Invalid log level: %s' % metricLevel)

setup_logger('simulator',cfg.logFilename, logLevel)
simulator = logging.getLogger('simulator')
setup_logger('metrics', cfg.metricFilename, metricLevel)
metrics = logging.getLogger('metrics')
globals.simulatorLogger = simulator
globals.metricLogger = metrics
# *** END OF LOGGING CONFIGURATIONS ***
