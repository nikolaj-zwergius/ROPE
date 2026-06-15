if __name__ != "__main__":
    from utils.def_class import Module, segmented_module
else:
    from def_class import Module, segmented_module

### Basic Modules
base = Module(name = 'base', file = 'helix_backbone.pdb', symbol = 'H1')
Helix = Module(name = 'Helix', file = 'helix_match.pdb', symbol = 'H2')
Crossover = Module(name = 'Crossover', file = 'crossover.pdb', symbol = 'X',sequence = ("NNN^NNNN"),len=7)
TetraLoop = Module(name = 'TetraLoop', file = 'Tetraloop.pdb', symbol = 'T',sequence = ("NUUCGN"),priority=2)
KissingLoop = Module(name = 'KissingLoop', file = 'KissingLoop.pdb', symbol = 'K',sequence = ("NNAANNNNNNANN"),priority=2)
### Fluorescent Modules


Broccoli = segmented_module(name = 'Broccoli', file = 'Brocolli_dye.pdb', symbol = 'B',sequence = ["GGACGGUCGGGUCCAG","CUGUCGAGUAGAGUGUGGGCU"],spacer = ["UUCG"],priority=2,ligand="2ZY")
#Mango = segmented_module(name = 'Mango', file = 'mango.pdb', symbol = 'M',sequence = ["GUGCGAAGGGACGGUGC","GGAGAGGAGAGCAC"],priority=2)
#Pepper = segmented_module(name = 'Pepper', file = 'pepper.pdb', symbol = 'P',sequence = ["part1","part2"],spacer =["UUCG"],priority=2)
#Cilivia = segmented_module(name = 'Cilivia', file = 'cilivia.pdb', symbol = 'C',sequence = ["part1","part2"],spacer =["UUCG"],priority=2)
#Squash = Module(name = 'Squash', file = 'squash.pdb', symbol = 'sQ',priority=2)
#Spinach = segmented_module(name = 'Spinach', file = 'spinach.pdb', symbol = 'sP',sequence = ["GUGAGGGUCGGGUCCAG","CUGUUGAGUAGAGUGUGGGCUC"],spacer = ["UUCG"],priority=2)

module_libary = {
    base.symbol:base,
    Helix.symbol: Helix,
    Crossover.symbol: Crossover,
    TetraLoop.symbol: TetraLoop,
    KissingLoop.symbol: KissingLoop,
    Broccoli.symbol: Broccoli,
    #Mango.symbol: Mango,
    #Pepper.symbol: Pepper,
    #Cilivia.symbol: Cilivia,
    #Spinach.symbol: Spinach,
    #Squash.symbol: Squash,
}

split_modules ={}

for module in module_libary.values():
    if isinstance(module, segmented_module):
        split_modules[module.symbol] = module