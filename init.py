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

gc.enable() #enable automatic garbage collection

random.seed()

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
