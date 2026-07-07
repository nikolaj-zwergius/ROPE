
kl_meta_list = {"A":"1",
                "B":"2",
                "C":"3",
                "D":"4",
                "E":"5",
                "F":"6",
                "G":"7",
                "H":"8",
                "I":"9",
                "1":"A",
                "2":"B",
                "3":"C",
                "4":"D",
                "5":"E",
                "6":"F",
                "7":"G",
                "8":"H",
                "9":"I",
                
                }

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
                   "B":{"C","G","U"},}
k_table = {"G":"U","U":"G"}
base_pairs_table = {"A":"U","U":"A","G":"CU","C":"G"}

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
change_base= {
    "A":(0,33,33,33),
    "C":(33,0,33,33),
    "G":(33,33,0,33),
    "U":(33,33,33,0),

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


flips =[((0),{"╰":"╭","╭":"╰","╯":"╮","╮":"╯","/":chr(92),chr(92):"/"},"Flipped file:"),
        ((1),{"╯":"╭","╮":"╰","╭":"╯","╰":"╮"},"Reversed file:"),
        ((0,1),{"╰":"╭","╭":"╰","╯":"╮","╮":"╯","/":chr(92),chr(92):"/"},"Reversed and Flipped file:")]

SUGAR_ATOMS = ['C3\'', 'C4\'', 'C5\'', 'O4\'',"P"]


from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]


FOLDER = ROOT/"data"/"RNA_lib"/"modules"
NT_FOLDER = ROOT/"data"/"RNA_lib"/"nucleotides"