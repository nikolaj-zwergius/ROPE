import rope.definitions.rope_def as rd
import rope.model.direction as di
import numpy as np

COMPLEMENT_WINDOW = 10
DUPLICATE_WINDOW = 10
KL_DELAY = 150

def generate_np_pattern(file:str) -> np.ndarray:
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

def find_5_prime(pattern:np.ndarray) -> tuple[int,int]:
    p5 = np.where(pattern=="5")
    p5 = (p5[0][0],p5[1][0])
    return p5

def get_backbone_start(pattern:np.ndarray) -> tuple[tuple[int,int],di.dirction]:
    p5 = find_5_prime(pattern)
    up, down, left, rigth = check_round(pattern, p5)
    if up.isalpha():
        return p5, (p5[0] - 1, p5[1]), di.dir_up()
    if down.isalpha():
        return p5, (p5[0] + 1, p5[1]), di.dir_down()
    if left.isalpha():
        return p5, (p5[0], p5[1] - 1), di.dir_left()
    if rigth.isalpha():
        return p5, (p5[0], p5[1] + 1), di.dir_rigth()
    raise ValueError("No valid first base")

def check(pattern:np.ndarray,id1:int,id2:int):
    try:
        return pattern[id1][id2]
    except IndexError:
        return ""

def check_round(pattern:np.ndarray,tup:tuple[int,int])->tuple[str,str,str,str]:
    up= check(pattern,tup[0]-1,tup[1])
    down= check(pattern,tup[0]+1,tup[1])
    left = check(pattern,tup[0],tup[1]-1)
    rigth = check(pattern,tup[0],tup[1]+1)
    return up,down,left,rigth

def reverse(seq:str) -> str:
    for char in seq:
        rev += rd.base_pairs_table[char][0]
        rev = rev[::-1]
    return rev


def map_structure(structure:str):
    structure.strip(".")
    mapping = [[]]*len(structure)
    stack1 = []
    stack2 = []
    stack3 = []
    for i in range(len(structure)):
        match structure[i]:
            case "(":
                stack1.append(i)
            case "[":
                stack2.append(i)
            case "{":
                stack3.append(i)
            case ")":
                mapping[i]=stack1.pop()
                mapping[mapping[i]] = i
            case "]":
                mapping[i]=stack2.pop()
                mapping[mapping[i]] = i
            case "}":
                mapping[i]=stack3.pop()
                mapping[mapping[i]] = i
            case _:
                mapping[i]=-1
    return mapping


def count_repeats(sequence:str, complement_window=COMPLEMENT_WINDOW, duplicate_window=DUPLICATE_WINDOW,bpmap:list|None=None):
    strand_length = len(sequence)
    repeat_map = ["-"] * strand_length
    pattern_repeats = 0
    poly_repeats = 0
    restriction_sites = 0

    for i in range(strand_length - complement_window + 1):
        block = sequence[i : i + complement_window]
        antisense = "".join(
            rd.base_pairs_table[base]
            for base in reversed(block)
        )
        j = sequence.find(antisense, i)
       
        while j != -1:
            for k in range(complement_window):
                if j+complement_window in bpmap:
                    #print(bpmap[j+complement_window-1-k]==i, bpmap[i+k] == j+complement_window-1)
                    continue
                repeat_map[i + k] = "P"
                repeat_map[j - k] = "P"
            j = sequence.find(antisense, j + 1)

    complement_zones = sum(1 for value in repeat_map if value == "P")

    for i in range(strand_length - duplicate_window + 1):
        block = sequence[i : i + duplicate_window]
        j = sequence.find(block, i + 1)
        while j != -1:
            for k in range(duplicate_window):
                repeat_map[i + k] = "D"
                repeat_map[j + k] = "D"
            j = sequence.find(block, j + 1)

    duplicate_zones = sum(1 for value in repeat_map if value == "D")

    for i in range(strand_length - 7):
        window = sequence[i : i + 8]
        if all(ch in {"A", "U"} for ch in window):
            pattern_repeats += 1
            for k in range(8):
                repeat_map[i + k] = "W"
        if all(ch in {"C", "G"} for ch in window):
            pattern_repeats += 1
            for k in range(8):
                repeat_map[i + k] = "S"

    for i in range(strand_length - 4):
        if sequence[i] == sequence[i + 1] == sequence[i + 2] == sequence[i + 3] == sequence[i + 4]:
            poly_repeats += 1
            for k in range(5):
                repeat_map[i + k] = sequence[i]

    for motif in rd.restriction_motifs:
        j = sequence.find(motif)
        while j != -1:
            restriction_sites += 1
            for k in range(len(motif)):
                repeat_map[j + k] = "X"
            j = sequence.find(motif, j + 1)

    return repeat_map, complement_zones, duplicate_zones, pattern_repeats, poly_repeats, restriction_sites


def build_barriers(structure_map:str, map_array:list, sequence_length:int):
    barriers = ["·"] * sequence_length
    topo_count = 0
    for i, ch in enumerate(structure_map):
        if ch == ".":
            barriers[i] = "·"
            topo_count = 0
        elif ch == "(":
            barriers[i] = "x"
            topo_count = 0
        elif ch == ")":
            partner = map_array[i]
            if partner < 0 or partner >= sequence_length:
                continue
            if barriers[partner] == "x":
                barriers[i] = "·"
                barriers[partner] = "·"
                topo_count = 0
            elif barriers[partner] == "X":
                if topo_count > 5:
                    barriers[i] = "X"
                    barriers[partner] = "~"
                else:
                    barriers[i] = "~"
                    barriers[partner] = "~"
                topo_count += 1
        if i > KL_DELAY and structure_map[i - KL_DELAY] == "]":
            partner = map_array[i - KL_DELAY]
            if 0 <= partner < sequence_length:
                barriers[i - KL_DELAY] = "·"
                barriers[partner] = "·"
                for k in range(partner, i - KL_DELAY):
                    if barriers[k] == "x":
                        barriers[k] = "X"
    return barriers