
from rope.model.Nucleotide import Nucleotide
from rope.definitions.rope_def import NT_FOLDER
from random import choices
### Nucleotides
A=Nucleotide(name = 'A', file = NT_FOLDER/'A.pdb', symbol = 'A')
C=Nucleotide(name = 'C', file = NT_FOLDER/'C.pdb', symbol = 'C')
G=Nucleotide(name = 'G', file = NT_FOLDER/'G.pdb', symbol = 'G')
U=Nucleotide(name = 'U', file = NT_FOLDER/'U.pdb', symbol = 'U')

nucleotide_libary:dict[str,Nucleotide] = {
                    A.symbol:A,
                    C.symbol:C,
                    G.symbol:G,
                    U.symbol:U,
                    "N":choices([A,C,G,U],k=1)[0]}


for nt in nucleotide_libary.values():
    nt.generate_cords()