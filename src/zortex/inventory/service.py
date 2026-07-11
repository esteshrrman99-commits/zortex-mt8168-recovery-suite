import json
from pathlib import Path
from .models import DeviceRecord
class DeviceInventory:
    def __init__(self,path='artifacts/device_inventory.json'):
        self.path=Path(path); self.path.parent.mkdir(parents=True,exist_ok=True)
    def load(self):
        if not self.path.exists(): return []
        return [DeviceRecord(**x) for x in json.loads(self.path.read_text())]
    def save(self,records):
        self.path.write_text(json.dumps([r.to_dict() for r in records],indent=2)+'\n')
    def upsert(self,record):
        records=[r for r in self.load() if r.device_id!=record.device_id]+[record]
        self.save(records); return records
