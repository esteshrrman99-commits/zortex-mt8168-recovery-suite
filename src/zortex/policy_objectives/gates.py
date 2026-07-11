from dataclasses import dataclass,asdict
@dataclass(frozen=True)
class GateResult:
    gate:str; passed:bool; evidence:str
    def to_dict(self): return asdict(self)
class RestorationGateEngine:
    REQUIRED_GATES=("device_identity_verified","usb_mode_identified",
    "partition_table_verified","backup_verified","artifact_hashes_verified",
    "boot_image_parsed","dtb_dtbo_verified","hardware_matrix_complete",
    "avb_chain_documented","rollback_indexes_recorded",
    "firmware_provenance_verified","partition_fit_verified",
    "vendor_compatibility_verified","authorized_trust_path_verified",
    "dry_run_verified","human_approval_recorded")
    def evaluate(self,evidence):
        r=[GateResult(g,bool(evidence.get(g,False)),
        "present" if evidence.get(g,False) else "missing") for g in self.REQUIRED_GATES]
        p=sum(x.passed for x in r)
        return {"status":"PASS" if p==len(r) else "BLOCKED","passed":p,
        "total":len(r),"results":[x.to_dict() for x in r]}
