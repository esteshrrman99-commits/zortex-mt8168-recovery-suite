from datetime import datetime,timezone
from hashlib import sha256
import hmac,json
class AttestationEngine:
    def attest(self,payload,secret):
        canonical=json.dumps(payload,sort_keys=True,separators=(',',':')).encode()
        return {'algorithm':'HMAC-SHA256','payload_sha256':sha256(canonical).hexdigest(),
        'signature':hmac.new(secret.encode(),canonical,sha256).hexdigest(),
        'attested_at':datetime.now(timezone.utc).isoformat()}
    def verify(self,payload,signature,secret):
        return hmac.compare_digest(self.attest(payload,secret)['signature'],signature)
