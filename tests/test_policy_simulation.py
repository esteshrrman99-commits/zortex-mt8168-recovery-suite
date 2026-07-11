from zortex.capability_registry.models import Capability
from zortex.capability_registry.service import CapabilityRegistry,BLOCK_MESSAGE
from zortex.simulations import SimulationEngine
from zortex.policy_objectives import RestorationGateEngine
from zortex.restoration_planner import RestorationPlanner
def test_registry(): assert {x.name.value for x in CapabilityRegistry().list()}=={x.value for x in Capability}
def test_simulation(): assert SimulationEngine().run(Capability.FLASH)["state_transition"]["hardware_changed"] is False
def test_blocked(): 
    d=CapabilityRegistry().evaluate(Capability.UNLOCK,simulation=False)
    assert d.hardware_execution_allowed is False and d.reason==BLOCK_MESSAGE
def test_gates(): assert RestorationGateEngine().evaluate({})["status"]=="BLOCKED"
def test_plan(): assert RestorationPlanner().build({})["hardware_execution"] is False
