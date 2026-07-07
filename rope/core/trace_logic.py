import sys,os
SCRIPT_DIR = os.path.abspath(__file__)
sys.path.append(os.path.dirname(SCRIPT_DIR))
import rope.definitions.rope_def as rd
from rope.core.grid_mapping import get_backbone_start, generate_np_pattern, check_round
from numpy import ndarray,int64
from pathlib import Path
from rope.io.blueprint_reader import parse_header


def base_pair_id(pattern:ndarray,tup:tuple[int,int]) -> tuple[None|tuple,None|str]:
    up,down,left,rigth = check_round(pattern,tup)
    if up in ["┊","!","*"]:
        return (tup[0]-2,tup[1]),up
    if down in ["┊","!","*"]:
        return (tup[0]+2,tup[1]),down
    if pattern[tup[0]][tup[1]] in rd.NUCLEOTIDE_CHARS:
        return None,"."
    if pattern[tup[0]][tup[1]] == "X":
        return None,"@"
    return None,None

def trace_backbone(pattern:ndarray,crossover:bool = False,header=None) -> tuple[str,str,dict,dict]:
    _, first, dir = get_backbone_start(pattern)
    #print(header)
    seq = ""
    base_pair =""
    next_base = first
    bracket0 =[]
    bracket1 =[]
    bracket2 =[]
    n_map = {}
    index = 0
    strand_dir = {}
    while pattern[next_base[0]][next_base[1]] != "3":
        strand_dir[next_base] = dir
        next_base_name = pattern[next_base[0]][next_base[1]]
        if next_base_name == " ":
            raise Exception
        match_id,match_type = base_pair_id(pattern,next_base)
        match match_type:
            case "*":
                if match_id not in bracket0 and next_base not in bracket0:
                    bracket0.append(match_id)
                    base_pair+="["
                if next_base in bracket0:
                    bracket0.pop()
                    base_pair+="]"
            case "!":
                if match_id not in bracket1 and next_base not in bracket1:
                    bracket1.append(match_id)
                    base_pair+="{"
                if next_base in bracket1:
                    bracket1.pop()
                    base_pair+="}"
            case "┊":
                if match_id not in bracket2 and next_base not in bracket2:
                    bracket2.append(match_id)
                    base_pair+="("
                if next_base in bracket2:
                    bracket2.pop()
                    base_pair+=")"
            case ".":
                base_pair+="."
            case "@":
                if header is None:
                    raise Exception("trying to use free KL without vaild @AB21 meta data")
                base_pair+="@"
            case _:
        
                pass
        if crossover and next_base_name == "^":
            seq+="^"
            base_pair+="^"
        if next_base_name in rd.NUCLEOTIDE_CHARS:
            seq+=next_base_name
            n_map[next_base] = index
            index +=1
        if next_base_name == "X":
            seq+="N"
            n_map[next_base] = index
            index +=1
        if next_base_name in dir.move_list.keys():
            dir=dir.move_list[next_base_name]()
        next_base = dir.move(next_base)
        
    return seq,base_pair,n_map,strand_dir





def trace_seq_into_backbone(seq:str,file: str|Path) -> ndarray:
    new_pattern = generate_np_pattern(file)
    _, first, dir = get_backbone_start(new_pattern)
    index = 0
    next_base = first
    while new_pattern[next_base[0]][next_base[1]] != "3":
        next_base_name = new_pattern[next_base[0]][next_base[1]]
        if next_base_name.isalpha():
            new_pattern[next_base[0]][next_base[1]] = seq[index]
            index+=1
        if next_base_name in dir.replace_list.keys():
            new_pattern[next_base[0]][next_base[1]] = dir.replace_list[next_base_name]
        if next_base_name in dir.move_list.keys():
            dir=dir.move_list[next_base_name]()
        next_base = dir.move(next_base)
    return new_pattern


