from RNA_lib.def_class import Module

### Basic Modules
Helix = Module(name = 'Helix', file = 'helix_backbone.pdb', symbol = 'H')
tetraHelix = Module(name = 'tetraHelix', file = 'aTetraloop.pdb', symbol = 'aT')
ptetraHelix = Module(name = 'ptetraHelix', file = 'pTetraloop.pdb', symbol = 'pT')
ltetraHelix = Module(name = 'ltetraHelix', file = 'lTetraloop.pdb', symbol = 'lT',sequence = ("NNUUCGNN"))
Crossover = Module(name = 'Crossover', file = 'crossover_backbone.pdb', symbol = 'X')
TetraLoop = Module(name = 'TetraLoop', file = 'Tetraloop.pdb', symbol = 'T',sequence = ("UUCG"))
KissingLoop = Module(name = 'KissingLoop', file = 'Kissingloop_backbone.pdb', symbol = 'K',sequence = ("AANNNNNNA"))
### Fluorescent Modules
Broccoli = Module(name = 'Broccoli', file = 'broccoli.pdb', symbol = 'B',sequence = ("part1","part2"))
Mango = Module(name = 'Mango', file = 'mango.pdb', symbol = 'M',sequence = ("part1","part2"))
Pepper = Module(name = 'Pepper', file = 'pepper.pdb', symbol = 'P',sequence = ("part1","part2"))
Cilivia = Module(name = 'Cilivia', file = 'cilivia.pdb', symbol = 'C',sequence = ("part1","part2"))
Squash = Module(name = 'Squash', file = 'squash.pdb', symbol = 'sQ',sequence = ("part1","part2"))
Spinach = Module(name = 'Spinach', file = 'spinach.pdb', symbol = 'sP',sequence = ("part1","part2"))

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

for module in module_libary.values():
    module.generate_cords()