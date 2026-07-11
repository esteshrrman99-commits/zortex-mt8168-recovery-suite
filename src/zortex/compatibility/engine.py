class CompatibilityEngine:
    WEIGHTS={'board_match':20,'chipset_match':15,'architecture_match':10,
    'partition_fit':15,'firmware_provenance':15,'avb_topology_match':10,
    'rollback_compatible':10,'vendor_compatible':5}
    def score(self,checks):
        earned=sum(v for k,v in self.WEIGHTS.items() if checks.get(k,False))
        blockers=[k for k in ('board_match','partition_fit','firmware_provenance') if not checks.get(k,False)]
        grade='S' if earned>=95 else 'A' if earned>=85 else 'B' if earned>=70 else 'C' if earned>=55 else 'D'
        return {'score':earned,'maximum':100,'grade':grade,'mandatory_blockers':blockers,
        'status':'COMPATIBLE' if earned>=85 and not blockers else 'REVIEW_REQUIRED','checks':checks}
