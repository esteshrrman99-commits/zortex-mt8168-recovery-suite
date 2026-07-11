from dataclasses import dataclass, asdict
@dataclass(frozen=True)
class DeviceRecord:
    device_id:str
    manufacturer:str='unknown'
    model:str='unknown'
    chipset:str='unknown'
    android_version:str='unknown'
    build_fingerprint:str='unknown'
    usb_mode:str='unknown'
    trust_state:str='unverified'
    def to_dict(self): return asdict(self)
