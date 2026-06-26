
from rope.model.Nucleotide import nucleotide
from rope.definitions.rope_def import NT_FOLDER
### Nucleotides
A=nucleotide(name = 'A', file = NT_FOLDER/'A.pdb', symbol = 'A')
C=nucleotide(name = 'C', file = NT_FOLDER/'C.pdb', symbol = 'C')
G=nucleotide(name = 'G', file = NT_FOLDER/'G.pdb', symbol = 'G')
U=nucleotide(name = 'U', file = NT_FOLDER/'U.pdb', symbol = 'U')

nucleotide_libary = {A.symbol:A,
                     C.symbol:C,
                     G.symbol:G,
                     U.symbol:U}


for nt in nucleotide_libary.values():
    nt.generate_cords()