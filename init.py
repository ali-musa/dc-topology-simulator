from base.event import *
from base.enum import *
from utils.helper import *

from topology.topology import *
from topology.fattree import *
from topology.jellyfish import *
from topology.nacre import *


from failure.failure import *
from reservation.tenant import *

import config as cfg

import random
import time
import traceback

# *** START OF LOGGING CONFIGURATIONS ***
import logging
logLevel = getattr(logging, cfg.logLevel.upper(), None)
logFilename = cfg.logFilename
if not isinstance(logLevel, int):
	raise ValueError('Invalid log level: %s' % logLevel)
# NOTE: append "%(asctime)s" to format attribute below for showing time of log
# message
# NOTE: append "%(levelname)s" to format attribute below for showing log level
# name
# NOTE: filemode='w' makes a new file every time.  remove this parameter to
# continue writing to same file every time.
logging.basicConfig(format='%(levelname)s : %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logLevel, filename=logFilename, filemode='w')
# *** END OF LOGGING CONFIGURATIONS ***