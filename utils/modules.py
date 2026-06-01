if __name__ != "__main__":
    from utils.def_class import Module, segmented_module
else:
    from def_class import Module, segmented_module
### Basic Modules
Helix = Module(name = 'Helix', file = 'helix_backbone.pdb', symbol = 'H')
tetraHelix = Module(name = 'tetraHelix', file = 'aTetraloop.pdb', symbol = 'aT')
ptetraHelix = Module(name = 'ptetraHelix', file = 'pTetraloop.pdb', symbol = 'pT')
ltetraHelix = Module(name = 'ltetraHelix', file = 'lTetraloop.pdb', symbol = 'lT',sequence = ("NNUUCGNN"))
Crossover = Module(name = 'Crossover', file = 'crossover.pdb', symbol = 'X')
TetraLoop = Module(name = 'TetraLoop', file = 'Tetraloop.pdb', symbol = 'T',sequence = ("UUCG"))
KissingLoop = Module(name = 'KissingLoop', file = 'Kissingloop_backbone.pdb', symbol = 'K',sequence = ("AANNNNNNA"))
### Fluorescent Modules
Broccoli = segmented_module(name = 'Broccoli', file = 'broccoli.pdb', symbol = 'B',sequence = ["part1","part2"],spacer = ["UUCG"])
Mango = segmented_module(name = 'Mango', file = 'mango.pdb', symbol = 'M',sequence = ["part1","part2"],spacer = ["UUCG"])
Pepper = segmented_module(name = 'Pepper', file = 'pepper.pdb', symbol = 'P',sequence = ["part1","part2"],spacer =["UUCG"])
Cilivia = segmented_module(name = 'Cilivia', file = 'cilivia.pdb', symbol = 'C',sequence = ["part1","part2"],spacer =["UUCG"])
Squash = Module(name = 'Squash', file = 'squash.pdb', symbol = 'sQ',)
Spinach = segmented_module(name = 'Spinach', file = 'spinach.pdb', symbol = 'sP',sequence = ["part1","part2"],spacer = ["UUCG"])

module_libary = {
    Helix.symbol: Helix,
    tetraHelix.symbol: tetraHelix,
    ptetraHelix.symbol: ptetraHelix,
    ltetraHelix.symbol: ltetraHelix,
    Crossover.symbol: Crossover,
    TetraLoop.symbol: TetraLoop,
    KissingLoop.symbol: KissingLoop,
    Broccoli.symbol: Broccoli,
    Mango.symbol: Mango,
    Pepper.symbol: Pepper,
    Cilivia.symbol: Cilivia,
    Spinach.symbol: Spinach,
    Squash.symbol: Squash,
}