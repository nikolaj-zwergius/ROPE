import numpy as np
one_letter_code = {"A":("A"),
                   "C":"C",
                   "G":"G",
                   "U":"U",
                   "T":"U",
                   "W":("U","A"),
                   "S":("C","G"),
                   "K":("U","G"),
                   "N":("C","G","U","G"),
                   "Y":{"C","U"},
                   "R":{"G","A"},
                   "M":{"A","C"},
                   "V":{"A","C","G"},
                   "H":{"A","C","U"},
                   "D":{"A","G","U"},
                   "B":{"C","G","U"}}

k_table = {"G":"U","U":"G"}
base_pairs_table = {"A":"U","U":"A","G":"C","C":"G"}

###(A,C,G,U)
mutation_rate = {"A":(100,0,0,0),
                   "C":(0,100,0,0),
                   "G":(0,0,100,0),
                   "U":(0,0,0,100),
                   "T":(0,0,0,100),
                   "W":(50,0,0,50),
                   "S":(0,50,50,0),
                   "K":(0,0,50,50),
                   "N":(25,25,25,25),
                   "Y":{"C","U"},
                   "R":{"G","A"},
                   "M":{"A","C"},
                   "V":{"A","C","G"},
                   "H":{"A","C","U"},
                   "D":{"A","G","U"},
                   "B":{"C","G","U"}}

class dirction():
    row = 0
    colum = 0
    move_list ={}
    def __int__(self,move_list):
        move_list = self.move_list
    def move(self,last_id):
        return (last_id[0]+self.row,last_id[1]+self.colum)
        
class dir_up(dirction):
    row = -1
    def __init__(self):
        super().__init__()
        self.move_list = {"╭":dir_rigth,
                    "╮":dir_left,
                    "/":dir_rigth,
                    chr(92):dir_left,}
        
    def __repr__(self):
        return "dir_up"
    
class dir_down(dirction):
    row = 1
    def __init__(self):
        super().__init__()
        self.move_list = {
                    "╯":dir_left,"╰":dir_rigth,
                    "/":dir_left,
                    chr(92):dir_rigth,}
    def __repr__(self):
        return "dir_down"
class dir_left(dirction):
    colum = -1
    def __init__(self):
        super().__init__()
        self.move_list = {"╭":dir_down,
                    "╰":dir_up,
                    "/":dir_down,
                    chr(92):dir_up,}
    def __repr__(self):
        return "dir_left"
class dir_rigth(dirction):
    colum = 1
    def __init__(self):
        super().__init__()
        self.move_list = {
                    "╮":dir_down,
                    "/":dir_up,
                    "╯":dir_up,
                    chr(92):dir_down,}
    def __repr__(self):
        return "dir_rigth"

def generate_np_pattern(file):
    with open(file, encoding="utf-8") as input_file:
        rows = 0
        colum = 0
        for line in input_file:
            if  not line.isspace():
                rows +=1
            line=line.rstrip()
            if len(line) >= colum:
                colum = len(line)
        rows -=1 
        pattern = np.full((rows,colum)," ")
        input_file.seek(0)
        line_index = 0
        for line in input_file:
            if line.startswith(">") or line.isspace():
                continue
            line = line.rstrip()
            for char_index,char in enumerate(line):
                pattern[line_index][char_index]=char
            line_index += 1
    return pattern

def find_5_prime(pattern:np.ndarray):
    p5 = np.where(pattern=="5")
    p5 = (p5[0][0],p5[1][0])
    return p5

def check(pattern,id1,id2):
    try:
        return pattern[id1][id2]
    except IndexError:
        return ""

def check_round(pattern,tup):
    up= check(pattern,tup[0]-1,tup[1])
    down= check(pattern,tup[0]+1,tup[1])
    left = check(pattern,tup[0],tup[1]-1)
    rigth = check(pattern,tup[0],tup[1]+1)
    return up,down,left,rigth

def reverse(seq):
    for char in seq:
        rev += base_pairs_table[char][0]
        rev = rev[::-1]
    return rev