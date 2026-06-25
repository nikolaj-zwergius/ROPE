
import sys
from pathlib import Path

# Add project root to Python path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import sys
import os
from io import TextIOWrapper
from numpy import ndarray, float32
from rope.utils.dim3_utils import umeyama
from rope.model.Module import get_sugar_cords, Module, segmented_module, inv_segmented_module
from rope.definitions.modules import module_libary, Helix
from rope.definitions.nucleotide import nucleotide_libary
from rope.core.trace_logic import trace_backbone
from rope.core.grid_mapping import generate_np_pattern, map_structure
from rope.core.module_mapper import module_mapper

import sys
from pathlib import Path

# Add project root to Python path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

def output_pdb(line:str,seq:str,index:int,line_index:int,align_residue:ndarray,atom_count:int,residue_count:int) -> str:
    line_string = list(line)
    line_string[6:11] = f"{atom_count:5d}"
    line_string[17:20] = f"{seq[index]:>3s}"
    line_string[22:26] = f"{residue_count:4d}"
    line_string[30:38] = f"{align_residue[line_index][0]:8.3f}"
    line_string[38:46] = f"{align_residue[line_index][1]:8.3f}"
    line_string[46:54] = f"{align_residue[line_index][2]:8.3f}"
    return "".join(line_string)

def output_ligand_pdb(line:str,align_atom:ndarray,ligand_index:int,atom_count:int):
    line_string = list(line)
    line_string[6:11] = f"{atom_count:5d}"
    line_string[22:26] = f"{ligand_index:4d}"
    line_string[30:38] = f"{align_atom[0]:8.3f}"
    line_string[38:46] = f"{align_atom[1]:8.3f}"
    line_string[46:54] = f"{align_atom[2]:8.3f}"
    return "".join(line_string)


def align_base_to_backbonde(f:TextIOWrapper,coord_dict:dict[ndarray],res_index:int,seq_index:int,seq:str,atom_count:int,aligment_variable:tuple[float32,ndarray,ndarray],residue_count:int) -> tuple[int,ndarray]:
    c,R,t=aligment_variable
    sugar_residue = get_sugar_cords(coord_dict[res_index])
    align_sugar = sugar_residue.dot(c*R)+t
    c2,R2,t2 = umeyama(nucleotide_libary[seq[seq_index]].start_cord,align_sugar)
    align_residue = nucleotide_libary[seq[seq_index]].build_cords[0].dot(c2*R2)+t2
    #print(nucleotide_libary[seq[seq_index]])
    for line_index,line in enumerate(nucleotide_libary[seq[seq_index]].build_lines[0]):
        f.write(output_pdb(line,seq,seq_index,line_index,align_residue,atom_count,residue_count))
        atom_count += 1
    return atom_count, align_sugar

def ligand_addtion(aligment_variable:tuple[float32,ndarray,ndarray],mod:Module,ligand_stack:list) -> list:
    c,R,t = aligment_variable
    aligned_lines =mod.ligand_coords[0].dot(c*R)+t
    ligand_stack.append((aligned_lines,mod.ligand_lines[0]))
    return ligand_stack

def ligand_printer(f:TextIOWrapper,ligand_stack:list,atom_count:int,seq:str) -> None:
    ligand_index = len(seq)+(100-len(seq)%100)
    for ligand in ligand_stack:
        for index in range(len(ligand[0])):
            f.write(output_ligand_pdb(ligand[1][index],ligand[0][index],ligand_index,atom_count))
        ligand_index +=1
    return

def length_test(Structure:list,seq:str):
    try:
        Structure_len = 1
        for i in range(1,len(Structure)):
            if Structure[i][0].isnumeric():
                Structure_len += len(module_libary[Structure[i][1:]].segments[int(Structure[i][0])])
                continue
            if Structure[i][0] == "i":
                Structure_len += len(module_libary[Structure[i][2:]].segments[int(Structure[i][1])])
                continue
            Structure_len += module_libary[Structure[i]].len
        assert Structure_len == len(seq)
    except AssertionError:
        print("Error: The length of the structure and sequence must be the same.")
        print(f"Length of structure: {Structure_len}, Length of sequence: {len(seq)}")
        exit(1)

def build_start(f:TextIOWrapper,seq:str,atom_count:int,build:list,residue_count:int,seq_index:int) -> tuple[int,ndarray,list,int,int]:
    for line in nucleotide_libary[seq].build_lines[0]:
        f.write("".join(line))
        atom_count+=1
    last_build = nucleotide_libary[seq].start_cord
    build[residue_count-1]=(last_build)
    #print(seq_index,seq[seq_index],residue_count)
    residue_count+=1
    seq_index += 1
    return atom_count,last_build,build,residue_count,seq_index

def build_non_seq_module(f:TextIOWrapper,mod:Module,build:list,align_var:tuple[int,ndarray,ndarray],seq:str,atom_count:int,residue_count:int,seq_index:int) -> tuple[int,ndarray,list,int,int]:
    for res_index,residue in enumerate(mod.build_cords):
        atom_count, aligned_sugar = align_base_to_backbonde(f,mod.coord_dict,res_index,seq_index,seq,atom_count,align_var,residue_count)
        build[residue_count-1] = aligned_sugar
        last_build = aligned_sugar
        #print(seq_index,seq[seq_index],residue_count)
        residue_count += 1
        seq_index += 1
    return atom_count,last_build,build,residue_count,seq_index

def build_seq_module(f:TextIOWrapper,mod:Module,build:list,align_value:tuple[int,ndarray,ndarray],seq:str,atom_count:int,residue_count:int,seq_index:int) -> tuple[int,ndarray,list,int,int]:
    c,R,t = align_value
    for res_index,residue in enumerate(mod.build_cords):
        aligned_sugar = get_sugar_cords(mod.coord_dict[res_index]).dot(c*R)+t
        align_residue = residue.dot(c*R)+t
        if mod.sequence[res_index] == "N":
            atom_count, aligned_sugar = align_base_to_backbonde(f,mod.coord_dict,res_index,seq_index,seq,atom_count,(c,R,t),residue_count)
        else:    
            for line_index,line in enumerate(mod.build_lines[res_index]):
                f.write(output_pdb(line,mod.sequence,res_index,line_index,align_residue,atom_count,residue_count))
                atom_count += 1
        build[residue_count-1] = aligned_sugar
        last_build = aligned_sugar
        residue_count += 1
        seq_index += 1
    return atom_count,last_build,build,residue_count,seq_index

def RNAbuild(file:str,output:str) -> None:
    pattern=generate_np_pattern(file)
    seq,base_pairs,_,_ = trace_backbone(pattern)
    mapping = map_structure(base_pairs)

    Structure:list = module_mapper(pattern)
    print(Structure)
    build = [None]*(len(seq)+1)
    ligand_stack = []
    module = Module
    length_test(Structure,seq)

    segment_stack={}

    with open(output, "w") as f:
        atom_count = 1
        residue_count = 1
        seq_index = 0
        for i in range(len(Structure)):
            if Structure[i] == "S":
                atom_count,last_build,build,residue_count,seq_index = build_start(f,seq[i],atom_count,build,residue_count,seq_index)

            elif Structure[i][0].isnumeric() or Structure[i][0]=="i":
                if Structure[i][0].isnumeric():
                    mod:segmented_module = module_libary[Structure[i][1:]]
                    offset = 0
                else:
                    mod:inv_segmented_module = module_libary[Structure[i][2:]].inverted()
                    offset = 1

                seg_index = int(Structure[i][0+offset])

                if Structure[i][0+offset] == "0":
                    last = last_build
                    if Structure[i][1+offset:] not in segment_stack:
                        segment_stack[Structure[i][1+offset:]] = []
                elif Structure[i][0+offset] == "1":
                    last = segment_stack[Structure[i][1+offset:]].pop(-1)
                
                

                assert type(mod) == inv_segmented_module or type(mod) == segmented_module
                mod.change_elements(seg_index)
                c,R,t = umeyama(mod.start_cord,last)
                atom_count,last_build,build,residue_count,seq_index = build_seq_module(f,mod,build,(c,R,t),seq,atom_count,residue_count,seq_index)
                mod.reset_elements()
                
                if Structure[i][0+offset] == "0":
                    segment_stack[Structure[i][1+offset:]].append(last_build)
                    if mod.ligand:
                        ligand_stack = ligand_addtion((c,R,t),mod,ligand_stack)
                elif Structure[i][1] =="0":
                    segment_stack[Structure[i][2:]].append(last_build)
                    if mod.ligand:
                        ligand_stack = ligand_addtion((c,R,t),mod,ligand_stack)
            elif Structure[i] == Helix.symbol:
                mod:Module = module_libary[Structure[i]]
                c,R,t = umeyama(mod.start_cord,build[mapping[residue_count-1]])
                atom_count,last_build,build,residue_count,seq_index =build_non_seq_module(f,mod,build,(c,R,t),seq,atom_count,residue_count,seq_index)
            else:
                mod = module_libary[Structure[i]]
                c,R,t = umeyama(module_libary[Structure[i]].start_cord,last_build)
                if mod.have_seq:
                    atom_count,last_build,build,residue_count,seq_index = build_seq_module(f,mod,build,(c,R,t),seq,atom_count,residue_count,seq_index)
                else:
                    atom_count,last_build,build,residue_count,seq_index =build_non_seq_module(f,mod,build,(c,R,t),seq,atom_count,residue_count,seq_index)
                if mod.ligand:
                    ligand_stack =ligand_addtion((c,R,t),mod,ligand_stack)

                build[residue_count-1] = last_build
        ligand_printer(f,ligand_stack,atom_count,seq)


def main():
        
    dir_path = os.path.dirname(os.path.realpath(__file__))  
    parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
    wd = os.getcwd()

    if len(sys.argv) < 1:
        print("Usage for specific files: batch_revolvr <file1> [<file2> ...]")
        print("Usage for all in folder: batch_revolvr")
        sys.exit(1)
    folder = f"{wd}/RNAbuild"
    if not os.path.exists(folder):
        os.makedirs(folder)

    args = sys.argv[1:]
    if len(args) == 0:
        for file in os.listdir():
            if not file.endswith(".txt"):
                continue
            else:
                RNAbuild(file,f"{folder}/{file.split(".")[0]}.pdb")
    else:
        for file in args:
            file = str(file.split(chr(92))[1])
            if not file.endswith(".txt"):
                print(f"{file} is not a .txt file it is {file.split(".")[:-1]}")
                continue
            if file in os.listdir():
                RNAbuild(file,f"{folder}/{file.split(".")[0]}.pdb")
            else:
                print(f"{file} not found in folder")
                  
if __name__ == "__main__":
    main()
