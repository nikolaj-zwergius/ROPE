import random
one_letter_code = {"A":("A"),
                   "C":"C",
                   "G":"G",
                   "U":"U",
                   "T":"U",
                   "W":("U","A"),
                   "S":("C","G"),
                   "K":("U","G"),
                   "N":("C","G","U","A"),
                   "Y":{"C","U"},
                   "R":{"G","A"},
                   "M":{"A","C"},
                   "V":{"A","C","G"},
                   "H":{"A","C","U"},
                   "D":{"A","G","U"},
                   "B":{"C","G","U"}}
k_table = {"G":"U","U":"G"}
base_pairs_table = {"A":"U","U":"A","G":"C","C":"G","N":"N"}

VALID_BASES = set(base_pairs_table.keys())
NUCLEOTIDE_CHARS = set(one_letter_code.keys())



mutation_rate = {   "A":(100,0,0,0),
                    "C":(0,100,0,0),
                    "G":(0,0,100,0),
                    "U":(0,0,0,100),
                    "T":(0,0,0,100),
                    "W":(50,0,0,50),
                    "S":(0,50,50,0),
                    "K":(0,0,50,50),
                    "N":(25,25,25,25),
                    "Y":(50,0,50,0),
                    "R":(0,50,0,50),
                    "M":(50,50,0,0),
                    "V":(33,33,33,0),
                    "H":(33,33,0,33),
                    "D":(33,0,33,33),
                    "B":(0,33,33,33)
                    }

restriction_motifs = [
        "GGUCUC",
        "GAGACC",
        "GAAGAC",
        "GUCUUC",
        "CGUCUC",
        "GAGACG",
        "GCUCUUC",
        "GAAGAGC",
        "AUCUGUU",
    ]




def mutate(mutation_rate:tuple[int,int,int,int])->str:
    new_base = random.choices(["A","C","G","U"],weights=mutation_rate)
    return new_base[0]
