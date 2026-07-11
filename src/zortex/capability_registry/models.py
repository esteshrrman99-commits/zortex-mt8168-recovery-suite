from __future__ import annotations
from dataclasses import dataclass,asdict
from enum import StrEnum
from typing import Any
class Capability(StrEnum):
    FLASH="flash"; ERASE="erase"; FORMAT="format"; UNLOCK="unlock"
    PAYLOAD="payload"; PATCH_SECURITY="patch-security"
    MODIFY_PRELOADER="modify-preloader"; DISABLE_VERIFICATION="disable-verification"
@dataclass(frozen=True)
class CapabilityRecord:
    name:Capability; category:str="device_service_research"; risk:str="critical"
    mode:str="simulation_only"; requires_authorized_trust_path:bool=True
    hardware_execution:bool=False
    def to_dict(self)->dict[str,Any]:
        d=asdict(self); d["name"]=self.name.value; return d
@dataclass(frozen=True)
class CapabilityDecision:
    capability:Capability; simulation_allowed:bool
    hardware_execution_allowed:bool; reason:str
    def to_dict(self)->dict[str,Any]:
        return {"capability":self.capability.value,
        "simulation_allowed":self.simulation_allowed,
        "hardware_execution_allowed":self.hardware_execution_allowed,
        "reason":self.reason}
