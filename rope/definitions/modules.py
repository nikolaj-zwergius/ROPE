from rope.model.Module import Module, segmented_module
from rope.definitions.rope_def import FOLDER
### Structual Modules
base = Module(name = 'base', file = FOLDER/'helix_backbone.pdb', symbol = 'H1')
Helix = Module(name = 'Helix', file = FOLDER/'helix_match.pdb', symbol = 'H2')
Crossover = Module(name = 'Crossover', file = FOLDER/'crossover.pdb', symbol = 'X',sequence = ("NNN^NNNN"),len=7)
TetraLoop = Module(name = 'TetraLoop', file = FOLDER/'Tetraloop.pdb', symbol = 'T',sequence = ("NUUCGN"),priority=2)
KissingLoop = Module(name = 'KissingLoop', file = FOLDER/'KissingLoop.pdb', symbol = 'K',sequence = ("NNAANNNNNNANN"),priority=2)


### Fluorescent Modules
Broccoli = segmented_module(name = 'Broccoli', file = FOLDER/'Brocolli_dye.pdb', symbol = 'B',sequence = ["GACGGUCGGGUCCAG","UGUCGAGUAGAGUGUGGGC"],spacer = ["CUUCG"],priority=2,ligand="2ZY")
#Mango = segmented_module(name = 'Mango', file = 'mango.pdb', symbol = 'M',sequence = ["GUGCGAAGGGACGGUGC","GGAGAGGAGAGCAC"],priority=2)
Pepper = segmented_module(name = 'Pepper', file = FOLDER/'Pepper.pdb', symbol = 'P',sequence = ["NNNACUGGCGCCNNN","NNNCAAUCGUGGCGUGUCGNNN"],spacer =["CCUUCGGG"],priority=2,ligand="J8L")
Cilivia = segmented_module(name = 'Cilivia', file = FOLDER/'cilivia.pdb', symbol = 'C',sequence = ["GAAGAUUGUAAACAUGC","GCAGACACUUC"],spacer =["CGAAAG"],priority=2,ligand="O2I")
Squash = Module(name = 'Squash', file = FOLDER/'squash.pdb', symbol = 'sQ',priority=3,sequence=("AUACAAGGUGAGCCCAAUAAUAUGGUUUGGGUUAGGAUAGGAAGUAGAGCCUUAAACUCUCUAAGCGGUAU"),ligand="2ZY")
#Spinach = segmented_module(name = 'Spinach', file = 'spinach.pdb', symbol = 'sP',sequence = ["GUGAGGGUCGGGUCCAG","CUGUUGAGUAGAGUGUGGGCUC"],spacer = ["UUCG"],priority=2)

module_libary:dict[str, Module|segmented_module] = {
    base.symbol:base,
    Helix.symbol: Helix,
    Crossover.symbol: Crossover,
    TetraLoop.symbol: TetraLoop,
    KissingLoop.symbol: KissingLoop,
    Broccoli.symbol: Broccoli,
    #Mango.symbol: Mango,
    Pepper.symbol: Pepper,
    Cilivia.symbol: Cilivia,
    #Spinach.symbol: Spinach,
    Squash.symbol: Squash,
}