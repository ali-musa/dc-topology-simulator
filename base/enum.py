class Enum(set):
	def __getattr__(self, name):
		if name in self:
			return name
		raise AttributeError

Status = Enum(["AVAILABLE", "IN_USE", "FAIL"])

CompType = Enum(["DEVICE", "LINK"])

EventType = Enum(["FAILURE","FAILURE_MSG", "RECOVERY", "RECOVERY_MSG", "BACKUP","ARRIVAL", "DEPARTURE", "END"]) #TODO: remove this enum, the event class already specifies type

TopologyType = Enum(["FATTREE", "JELLYFISH", "NACRE" , "CUSTOM"])

FailureType = Enum(["PHILLIPA"])

TrafficPriority = Enum(["HIGH", "NORMAL", "LOW"])

BackupStrategy = Enum(["NONE", "TOR_TO_TOR", "END_TO_END", "FLEXIBLE_REPLICA"])

TrafficType  = Enum(["FLOW", "TENANT"])

AllocationStrategy = Enum(["RANDOM_SOURCE_DESTINATION", "OKTOPUS"])

TrafficCharacteristics = Enum(["UNIFORM_RANDOM"])