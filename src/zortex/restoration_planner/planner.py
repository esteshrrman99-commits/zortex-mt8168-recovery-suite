from zortex.policy_objectives import RestorationGateEngine
class RestorationPlanner:
    def __init__(self): self.gates=RestorationGateEngine()
    def build(self,evidence):
        r=self.gates.evaluate(evidence)
        return {"gate_result":r,
        "plan_status":"READY_FOR_DOCUMENTED_REVIEW" if r["status"]=="PASS" else "BLOCKED",
        "steps":["Review evidence manifest","Review compatibility report",
        "Review trust-path documentation","Record human approval",
        "Produce non-executable restoration plan"],"hardware_execution":False}
