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



