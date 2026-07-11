class PluginManager:
    def __init__(self): self._plugins={}
    def register(self,plugin): self._plugins[plugin.name]=plugin
    def run_all(self,context): return {n:p.analyze(context) for n,p in self._plugins.items()}
