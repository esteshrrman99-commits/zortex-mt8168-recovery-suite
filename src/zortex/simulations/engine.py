from datetime import datetime,timezone
from zortex.capability_registry.service import CapabilityRegistry
class SimulationEngine:
    def __init__(self): self.registry=CapabilityRegistry()
    def run(self,capability):
        d=self.registry.evaluate(capability,simulation=True)
        return {"generated_at":datetime.now(timezone.utc).isoformat(),
        "capability":capability.value,"mode":"simulation","decision":d.to_dict(),
        "state_transition":{"before":"unassessed","after":"simulated",
        "hardware_changed":False}}
