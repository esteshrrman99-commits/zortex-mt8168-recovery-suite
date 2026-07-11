from datetime import datetime,timezone
from hashlib import sha256,sha512
from pathlib import Path
import json,shutil
class EvidenceCollector:
    def __init__(self,root='artifacts/evidence'):
        self.root=Path(root); self.root.mkdir(parents=True,exist_ok=True)
    def capture_file(self,source,label='artifact'):
        src=Path(source)
        if not src.is_file(): raise FileNotFoundError(src)
        stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
        out=self.root/stamp; out.mkdir(parents=True,exist_ok=True)
        dst=out/src.name; shutil.copy2(src,dst); data=dst.read_bytes()
        record={'label':label,'source_name':src.name,'stored_path':str(dst),
        'size_bytes':len(data),'sha256':sha256(data).hexdigest(),
        'sha512':sha512(data).hexdigest(),'captured_at':datetime.now(timezone.utc).isoformat()}
        (out/'manifest.json').write_text(json.dumps(record,indent=2)+'\n')
        return record
