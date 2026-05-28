import numpy as np
from RNA_lib.def_class import nucleotide

### Nucleotides
A=nucleotide(name = 'A', file = 'A.pdb', symbol = 'A')
C=nucleotide(name = 'C', file = 'C.pdb', symbol = 'C')
G=nucleotide(name = 'G', file = 'G.pdb', symbol = 'G')
U=nucleotide(name = 'U', file = 'U.pdb', symbol = 'U')

nucleotide_libary = {A.symbol:A,
                     C.symbol:C,
                     G.symbol:G,
                     U.symbol:U}


for nt in nucleotide_libary.values():
    nt.generate_cords()