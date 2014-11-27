class Enum(set):
	def __getattr__(self, name):
		if name in self:
			return name
		raise AttributeError

Status = Enum(["AVAILABLE", "IN_USE", "FAIL"])

CompType = Enum(["DEVICE", "LINK"])

EventType = Enum(["FAILURE", "RECOVERY", "ARRIVAL", "DEPARTURE", "END"])

TopologyType = Enum(["FATTREE", "JELLYFISH", "NACRE" , "CUSTOM"])

FailureType = Enum(["PHILLIPA"])

TrafficPriority = Enum(["HIGH", "NORMAL", "LOW"])

BackupStrategy = Enum(["NONE", "TOR_TO_TOR", "END_TO_END"])

AllocationStrategy  = Enum(["FLOW", "OKTOPUS"])