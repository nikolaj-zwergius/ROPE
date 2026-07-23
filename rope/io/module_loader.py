from rope.io.toml_io import load_toml
from rope.model.Module import Module, segmented_module
from rope.definitions.rope_def import ROOT
def load_module(path,wanted_variant):
    path =  ROOT/"data/RNA_lib/modules"/path
    toml = load_toml(path/"module.toml")
    meta:dict = toml.get("metadata",{})
    module:dict = toml.get("module",{})
    variant:dict = toml.get(wanted_variant,{})
    if variant == {}:
        defualt = toml.get("default",{})
        if wanted_variant == defualt.get("name"):
            variant = defualt
        else:
            raise KeyError("Invalid ligand given")

    name = meta.get("name","")
    symbol = module.get("symbol","")
    sequence= module.get("sequence",None)
    priority = int(module.get("priority",0))
    nonstandard = bool(module.get("nonstandard",False))
    file = path/variant.get("file","")
    module_type= module.get("type")
    ligand = variant.get("ligand",None)


    if module_type == "module":
        mod =Module(name,file,symbol,sequence,priority,nonstandard,ligand)
    elif module_type == "segmented":
        sequence = module.get("segments",[])
        spacer = module.get("spacer",[])
        mod = segmented_module(name,file,symbol,sequence,spacer,priority,ligand)
    else:
        raise TypeError("No valid type for module is given")
    return mod