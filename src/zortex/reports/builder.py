from datetime import datetime,timezone
from pathlib import Path
import json
class ReportBuilder:
    def build(self,title,sections,out_dir='reports/elite'):
        out=Path(out_dir); out.mkdir(parents=True,exist_ok=True)
        stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
        payload={'title':title,'generated_at':datetime.now(timezone.utc).isoformat(),'sections':sections}
        jp=out/f'{stamp}.json'; mp=out/f'{stamp}.md'
        jp.write_text(json.dumps(payload,indent=2)+'\n')
        lines=[f'# {title}','',f"Generated: {payload['generated_at']}",'']
        for name,content in sections.items():
            lines += [f'## {name}','','```json',json.dumps(content,indent=2),'```','']
        mp.write_text('\n'.join(lines))
        return {'json':str(jp),'markdown':str(mp)}
