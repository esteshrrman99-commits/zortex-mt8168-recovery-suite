from zortex.attestation import AttestationEngine
from zortex.compatibility import CompatibilityEngine
from zortex.inventory import DeviceInventory,DeviceRecord
from zortex.provenance import ProvenanceGraph
from zortex.plugins import PluginManager,ZortexPlugin
def test_compatibility():
    r=CompatibilityEngine().score({'board_match':True,'partition_fit':True,'firmware_provenance':True})
    assert r['mandatory_blockers']==[]
def test_attestation():
    e=AttestationEngine(); p={'device':'demo'}; s=e.attest(p,'secret')['signature']; assert e.verify(p,s,'secret')
def test_inventory(tmp_path):
    i=DeviceInventory(tmp_path/'i.json'); i.upsert(DeviceRecord('1',model='711')); assert i.load()[0].model=='711'
def test_graph(tmp_path):
    g=ProvenanceGraph(); a=g.add_node('device',{'id':'1'}); b=g.add_node('evidence',{'id':'2'}); g.link(a,'produced',b); assert len(g.export(tmp_path/'g.json')['edges'])==1
def test_plugins():
    class Demo(ZortexPlugin):
        name='demo'
        def analyze(self,context): return {'ok':context['ok']}
    m=PluginManager(); m.register(Demo()); assert m.run_all({'ok':True})['demo']['ok']
