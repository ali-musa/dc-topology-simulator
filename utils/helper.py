import time
import logging

class helper():
	@staticmethod
	def print_timing(func):
		def wrapper(*args, **kwargs):
			t1 = time.time()
			res = func(*args, **kwargs)
			t2 = time.time()
			diff = t2 - t1
			if func.func_name == 'main':
				minutes = int(diff / 60.0)
				seconds = diff - (minutes * 60)
				logging.debug('The simulation took %0.3f ms = %d min and %0.3f sec\n' % (diff * 1000, minutes, seconds))
			else:
				logging.debug('%s() took %0.3f ms' % (func.func_name, diff * 1000.0))
			return res
		return wrapper

	@staticmethod
	def sortedInsert(event, events):
		# this method is used to insert sorted events in the event queue on the basis of their time of occurence
		if event is not None:
			time = event.getEventTime()
			numEvents = len(events)
			for i in range(numEvents):
				if events[i].getEventTime() > time:
					events.insert(i, event)
					break

	@staticmethod
	def findValue(line, param):
		# this method is used while parsin custom topology input
		i = 0
		for l in line:
			if l == param:
				return line[i + 1]
			i+=1
		return None