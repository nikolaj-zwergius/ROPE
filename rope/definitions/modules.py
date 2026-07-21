#from rope.model.Module import Module, segmented_module
#from rope.definitions.rope_def import FOLDER
#### Structual Modules
#base = Module(name = 'base', file = FOLDER/"structural"/"helix_free"/'helix_backbone.pdb', symbol = 'H1',nonstandard =True)
#Helix = Module(name = 'Helix', file = FOLDER/"structural"/"helix_paired"/'helix_match.pdb', symbol = 'H2',nonstandard =True)
#Crossover = Module(name = 'Crossover', file = FOLDER/"structural"/"crossover"/'crossover.pdb', symbol = 'X',sequence = ("NNN^NNNN"),nonstandard =True)
#TetraLoop = Module(name = 'TetraLoop', file = FOLDER/"structural"/"tetraloop"/'Tetraloop.pdb', symbol = 'T',sequence = ("NUUCGN"),priority=2)
#KissingLoop = Module(name = 'KissingLoop', file = FOLDER/"structural"/"kissingloop"/'KissingLoop.pdb', symbol = 'K',sequence = ("NNAANNNNNNANN"),priority=2)


### Fluorescent Modules
#Broccoli = segmented_module(name = 'Broccoli', file = FOLDER/"fluorescent"/"brocolli"/'Brocolli_DFHBI-1T.pdb', symbol = 'B',sequence = ["GACGGUCGGGUCCAG","UGUCGAGUAGAGUGUGGGC"],spacer = ["CUUCG"],priority=2,ligand="2ZY")
#Pepper = segmented_module(name = 'Pepper', file = FOLDER/"fluorescent"/"pepper"/'Pepper_6HBC.pdb', symbol = 'P',sequence = ["NNNACUGGCGCCNNN","NNNCAAUCGUGGCGUGUCGNNN"],spacer =["CCUUCGGG"],priority=2,ligand="J8L")
#Cilivia = segmented_module(name = 'Cilivia', file = FOLDER/"fluorescent"/"cilivia"/'cilivia_N618.pdb', symbol = 'C',sequence = ["GAAGAUUGUAAACAUGC","GCAGACACUUC"],spacer =["CGAAAG"],priority=2,ligand="O2I")
#Squash = Module(name = 'Squash', file = FOLDER/"fluorescent"/"squash"/'squash_DFHBI-1T.pdb', symbol = 'sQ',priority=3,sequence=("AUACAAGGUGAGCCCAAUAAUAUGGUUUGGGUUAGGAUAGGAAGUAGAGCCUUAAACUCUCUAAGCGGUAU"),ligand="2ZY")
#Spinach = segmented_module(name = 'Spinach', file = 'spinach.pdb', symbol = 'sP',sequence = ["GUGAGGGUCGGGUCCAG","CUGUUGAGUAGAGUGUGGGCUC"],spacer = ["UUCG"],priority=2)
#Rhoblast
#Chili
#ispinach
#Corn
#Beetroot
#theophylline
#dopamine
#quinine-I
#THF
#SAM-I
#SAM-V
#thombin
#FMN
#5hyrdotryptophan
#oxoguanine
#neomycin


#Mango = segmented_module(name = 'Mango', file = 'mango.pdb', symbol = 'M',sequence = ["GUGCGAAGGGACGGUGC","GGAGAGGAGAGCAC"],priority=2)
#imango-III
#Mango2
#mango-III
#Mango-IV

### Binding Aptameres




#ATP bidnign
#AMP
#TMR
#MalichteGreen
#GTPI
#B12
#BPP (bovine prion protein)
#GTPV
#preQ1 +- metabolite
#2OOM Hiv aptamer??

#TTP
#DGR-1B
#NFkB
#rev
#xpt-pbuX guanine
#DASR
#M6/PPDA
#M6C
#HTLV-1
#S6
#Mbox
#cobalmin
#adine riboswitch
#guanine
#TetR
#Preq0
#tobramycin
#falvin redox
#quinie-I
#tretraclycin
#DIR2
#Arginine
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

#lycine-glycin











#module_libary:dict[str,Module|segmented_module] = {
#    base.symbol:base,
#    Helix.symbol: Helix,
#    Crossover.symbol: Crossover,
#    TetraLoop.symbol: TetraLoop,
#    KissingLoop.symbol: KissingLoop,
#    #Broccoli.symbol: Broccoli,
#    #Mango.symbol: Mango,
#    #Pepper.symbol: Pepper,
#    #Cilivia.symbol: Cilivia,
#    #Spinach.symbol: Spinach,
#    #Squash.symbol: Squash,
#}
#
#named_module_libary:dict[str,Module|segmented_module] = {}
#for i in module_libary:
#    if module_libary[i].ligand:
#        named_module_libary[module_libary[i].name] = module_libary[i]
#