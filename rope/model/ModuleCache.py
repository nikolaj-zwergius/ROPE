from collections.abc import Mapping

from rope.io.module_loader import load_module
from rope.model.Module import Module
from rope.model.records import IndexEntry

class ModuleCache:

    """Reuse module instances by ``(symbol, requested_variant)`` key.

    The index supplies the module path and name; absent ligand selections use
    the ``"default"`` variant. Cached instances are shared by all callers using
    the same key.
    """

    def __init__(self, index_library: Mapping[str, IndexEntry]) -> None:
        self.index_library = index_library
        self.index_libary_name_key = {}
        self.cache: dict[tuple[str, str], Module] = {}

    def get_module(self, symbol: str, ligands: Mapping[str, str]) -> Module:
        name  =  self.index_library[symbol].name
        variant = ligands.get(name, "default")
        key = (symbol, variant)

        if key not in self.cache:
            self.cache[key] = self.load_module(key)

        return self.cache[key]
    
    def load_module(self, key: tuple[str, str]) -> Module:
        path = self.index_library[key[0]].path
        mod  = load_module(path,key[1])
        return mod


    