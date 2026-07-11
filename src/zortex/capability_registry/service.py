from .models import Capability,CapabilityDecision,CapabilityRecord
BLOCK_MESSAGE="BLOCKED: authorized restoration gate has not been satisfied."
class CapabilityRegistry:
    def __init__(self): self._records={c:CapabilityRecord(c) for c in Capability}
    def list(self): return list(self._records.values())
    def evaluate(self,capability,*,authorized_trust_path_verified=False,simulation=True):
        if simulation:
            return CapabilityDecision(capability,True,False,"Simulation and policy analysis are permitted.")
        if not authorized_trust_path_verified:
            return CapabilityDecision(capability,True,False,BLOCK_MESSAGE)
        return CapabilityDecision(capability,True,False,
        "Trust evidence recorded; no device-mutating adapters are present.")
