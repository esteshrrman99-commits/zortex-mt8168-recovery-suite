from zortex.sdk_dashboard import *

def test_profile_registry(tmp_path):
    r=DeviceProfileRegistry(tmp_path/"p.json")
    r.upsert(DeviceProfile("p1","Vendor","Model","Chip","arm64","10"))
    assert r.get("p1").model=="Model"

def test_timeline(tmp_path):
    t=EvidenceTimeline(tmp_path/"t.jsonl")
    t.append("probe","done")
    assert t.read()[0]["event_type"]=="probe"

def test_kb(tmp_path):
    k=KnowledgeBase(tmp_path/"kb")
    k.add("MT8168","chipset","MediaTek notes",["mediatek"])
    assert k.search("mediatek")[0]["title"]=="MT8168"

def test_sdk():
    class Demo(ZortexSDKPlugin):
        name="demo"; version="1.0"
        def run(self,context): return {"device":context.device_id}
    r=ZortexSDKRuntime(); r.register(Demo())
    assert r.execute(ZortexContext("d1","s1"))["demo"]["result"]["device"]=="d1"

def test_dashboard(tmp_path):
    p=tmp_path/"index.html"
    DashboardBuilder().build([],[],[],[],p)
    assert "ZORTEX Command Dashboard" in p.read_text()

def test_health():
    assert "python" in HealthChecker().run()
