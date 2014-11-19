import link
import device

class Path:
	def __init__(self, _id, _label, _isPrimary):
		self.id = _id
		self.label = _label
		self.isPrimary = _isPrimary
		self.beingUsed = not _isPrimary
		self.devices = []
		self.links = []

# Utility functions
	def generatePath(src, dst):
		print "Generating path"
		
