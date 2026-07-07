from rope.model.Module import Module, segmented_module
from rope.definitions.rope_def import FOLDER
### Structual Modules
base = Module(name = 'base', file = FOLDER/'helix_backbone.pdb', symbol = 'H1')
Helix = Module(name = 'Helix', file = FOLDER/'helix_match.pdb', symbol = 'H2')
Crossover = Module(name = 'Crossover', file = FOLDER/'crossover.pdb', symbol = 'X',sequence = ("NNN^NNNN"),len=7)
TetraLoop = Module(name = 'TetraLoop', file = FOLDER/'Tetraloop.pdb', symbol = 'T',sequence = ("NUUCGN"),priority=2)
KissingLoop = Module(name = 'KissingLoop', file = FOLDER/'KissingLoop.pdb', symbol = 'K',sequence = ("NNAANNNNNNANN"),priority=2)
#kissingloop120
#AUCGCA
#ACAUAGA
#TAR-TAR


### Fluorescent Modules
Broccoli = segmented_module(name = 'Broccoli', file = FOLDER/'Brocolli_dye.pdb', symbol = 'B',sequence = ["GACGGUCGGGUCCAG","UGUCGAGUAGAGUGUGGGC"],spacer = ["CUUCG"],priority=2,ligand="2ZY")
#Mango = segmented_module(name = 'Mango', file = 'mango.pdb', symbol = 'M',sequence = ["GUGCGAAGGGACGGUGC","GGAGAGGAGAGCAC"],priority=2)
Pepper = segmented_module(name = 'Pepper', file = FOLDER/'Pepper.pdb', symbol = 'P',sequence = ["NNNACUGGCGCCNNN","NNNCAAUCGUGGCGUGUCGNNN"],spacer =["CCUUCGGG"],priority=2,ligand="J8L")
Cilivia = segmented_module(name = 'Cilivia', file = FOLDER/'cilivia.pdb', symbol = 'C',sequence = ["GAAGAUUGUAAACAUGC","GCAGACACUUC"],spacer =["CGAAAG"],priority=2,ligand="O2I")
Squash = Module(name = 'Squash', file = FOLDER/'squash.pdb', symbol = 'sQ',priority=3,sequence=("AUACAAGGUGAGCCCAAUAAUAUGGUUUGGGUUAGGAUAGGAAGUAGAGCCUUAAACUCUCUAAGCGGUAU"),ligand="2ZY")
#Spinach = segmented_module(name = 'Spinach', file = 'spinach.pdb', symbol = 'sP',sequence = ["GUGAGGGUCGGGUCCAG","CUGUUGAGUAGAGUGUGGGCUC"],spacer = ["UUCG"],priority=2)
#Rhoblast
#Chili
#ispinach
#imango-III
#Mango2
#mango-III
#Corn
#Mango-IV

### Binding Aptameres

#MS2
#PP7
#TAR/TAT
#L7Ae
#TMR
#MalichteGreen
#theophylline
#GTPI
#B12
#dopamine
#AMP
#BPP (bovine prion protein)
#GTPV
#preQ1 +- metabolite
#2OOM Hiv aptamer??
#ATP bidnign
#5hyrdotryptophan
#hydroforlate
#TTP
#DGR-1B
#NFkB
#rev
#xpt-pbuX guanine
#DASR
#neomycin
#M6/PPDA
#M6C
#THF
#oxoguanine
#HTLV-1
#S6
#Mbox
#cobalmin
#adine riboswitch
#FMN
#guanine
#TetR
#Preq0
#tobramycin
#Beetroot
#falvin redox
#quinie-I
#tretraclycin
#DIR2
#Arginine
#SAM-I
#SAM-V
#anti-prion
#AML1 runt domin
#minF-lyzome
#GCPI
#bromolignd
#trifluroethyl-ligand
#2deoxygunine
#cituline
#yjdF riboswitch
#YmaH
#FMN
#strptomycin
#HIV REV
#gcouple-reseptor
#fluoride
#Human IXa
#glycin
#NAD-II
#ZTP
#c-di-GMP-I
#DesGla-XaS195A
#2-dG-III
#c-di-GMP-II
#biotin
#lycine-glycin
#thombin










module_libary:dict[str,Module|segmented_module] = {
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

named_module_libary:dict[str,Module|segmented_module] = {}
for i in module_libary:
    if module_libary[i].ligand:
        named_module_libary[module_libary[i].name] = module_libary[i]