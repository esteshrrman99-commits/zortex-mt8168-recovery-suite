from datetime import datetime,timezone
from hashlib import sha256
from pathlib import Path
import json
class ProvenanceGraph:
    def __init__(self): self.nodes=[]; self.edges=[]
    def add_node(self,kind,data):
        node_id=sha256(json.dumps({'kind':kind,'data':data},sort_keys=True).encode()).hexdigest()[:20]
        self.nodes.append({'id':node_id,'kind':kind,'data':data,'created_at':datetime.now(timezone.utc).isoformat()})
        return node_id
    def link(self,source,relation,target): self.edges.append({'source':source,'relation':relation,'target':target})
    def export(self,path):
        payload={'schema_version':'1.0','nodes':self.nodes,'edges':self.edges}
        Path(path).parent.mkdir(parents=True,exist_ok=True)
        Path(path).write_text(json.dumps(payload,indent=2)+'\n')
        return payload
