from rope.io.module_loader import load_module

class ModuleCache:

    def __init__(self, index_library):
        self.index_library = index_library
        self.cache = {}

    def get_module(self, symbol, ligands):
        variant = ligands.get(symbol, "default")
        key = (symbol, variant)

        if key not in self.cache:
            self.cache[key] = self.load_module(key)

        return self.cache[key]
    
    def load_module(self,key):
        path = self.index_library[key[0]].path
        mod  = load_module(path,key[1])
        return mod


    