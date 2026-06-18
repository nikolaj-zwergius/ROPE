import sys
import os
from utils.dim3_utils import umeyama
from utils.def_class import get_sugar_cords, Module, segmented_module
from utils.modules import module_libary, Helix
from utils.nucleotide import nucleotide_libary
from trace_pattern import trace_backbone
from utils.trace_utils import generate_np_pattern, map_structure
from utils.module_mapper import module_mapper

def output_pdb(line,seq,index,line_index,align_residue,atom_count,residue_count):
    line_string = list(line)
    line_string[6:11] = f"{atom_count:5d}"
    line_string[17:20] = f"{seq[index]:>3s}"
    line_string[22:26] = f"{residue_count:4d}"
    line_string[30:38] = f"{align_residue[line_index][0]:8.3f}"
    line_string[38:46] = f"{align_residue[line_index][1]:8.3f}"
    line_string[46:54] = f"{align_residue[line_index][2]:8.3f}"
    return "".join(line_string)

def output_ligand_pdb(line,align_atom,ligand_index,atom_count):
    line_string = list(line)
    line_string[6:11] = f"{atom_count:5d}"
    line_string[22:26] = f"{ligand_index:4d}"
    line_string[30:38] = f"{align_atom[0]:8.3f}"
    line_string[38:46] = f"{align_atom[1]:8.3f}"
    line_string[46:54] = f"{align_atom[2]:8.3f}"
    return "".join(line_string)

def align_base_to_backbonde(f,coord_dict,res_index,seq_index,seq,atom_count,aligment_variable,residue_count):
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

def ligand_addtion(f,aligment_variable,mod:Module,ligand_stack:list):
    c,R,t = aligment_variable
    aligned_lines =mod.ligand_coords[0].dot(c*R)+t
    ligand_stack.append((aligned_lines,mod.ligand_lines[0]))

def ligand_printer(f,ligand_stack,atom_count,seq):
    ligand_index = len(seq)+(100-len(seq)%100)
    for ligand in ligand_stack:
        for index in range(len(ligand[0])):
            f.write(output_ligand_pdb(ligand[1][index],ligand[0][index],ligand_index,atom_count))
        ligand_index +=1
    return

def RNAbuild(file,output):
    pattern=generate_np_pattern(file)
    seq,base_pairs,_,_ = trace_backbone(pattern)
    mapping = map_structure(base_pairs)

    Structure:str = module_mapper(pattern)
    print(Structure)
    build = [None]*(len(seq)+1)
    ligand_stack = []
    module = Module
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

    segment_stack={}

    with open(output, "w") as f:
        atom_count = 1
        residue_count = 1
        seq_index = 0
        for i in range(len(Structure)):
            if Structure[i] == "S":
                for line in nucleotide_libary[seq[i]].build_lines[0]:
                    f.write("".join(line))
                    atom_count+=1
                last_build = nucleotide_libary[seq[i]].start_cord
                build[residue_count-1]=(last_build)
                #print(seq_index,seq[seq_index],residue_count)
                residue_count+=1
                seq_index += 1

            elif Structure[i][0].isnumeric() or Structure[i][0]=="i":
                if Structure[i][0] == "0":
                    last = last_build
                    if Structure[i][1:] not in segment_stack:
                        segment_stack[Structure[i][1:]] = []
                elif Structure[i][0] == "i" and Structure[i][1] == "0":
                    last = last_build
                    if Structure[i][2:] not in segment_stack:
                        segment_stack[Structure[i][2:]] = []
                elif Structure[i][0] == "i" and Structure[i][1] == "1":
                    last = segment_stack[Structure[i][2:]].pop(-1)
                else:
                    last = segment_stack[Structure[i][1:]].pop(-1)
                
                if Structure[i][0].isnumeric():
                    seg_index = int(Structure[i][0])
                    mod:segmented_module = module_libary[Structure[i][1:]]
                else:
                    seg_index = int(Structure[i][1])
                    mod:segmented_module = module_libary[Structure[i][2:]].inverted()
                c,R,t = umeyama(mod.segment_start_cord[seg_index],last)
                for res_index,residue in enumerate(mod.segment_build_cords[seg_index]):
                    aligned_sugar = get_sugar_cords(mod.segment_coord_dict[seg_index][res_index]).dot(c*R)+t
                    align_residue = residue.dot(c*R)+t
                    if mod.segments[seg_index][res_index] == "N":
                        atom_count, aligned_sugar = align_base_to_backbonde(f,mod.segment_coord_dict[seg_index],res_index,seq_index,seq,atom_count,(c,R,t),residue_count)
                    else:
                        #print(mod.segments[seg_index][res_index],seq[seq_index],res_index,residue_count)
                        for line_index,line in enumerate(mod.segment_build_lines[seg_index][res_index]):
                            f.write(output_pdb(line,mod.segments[seg_index],res_index,line_index,align_residue,atom_count,residue_count))
                            atom_count += 1
                    build[residue_count-1] = aligned_sugar
                    last_build = aligned_sugar
                    #print(seq_index,seq[seq_index],residue_count,mod.sequence[res_index])
                    residue_count += 1
                    seq_index += 1
                if Structure[i][0] == "0":
                    segment_stack[Structure[i][1:]].append(last_build)
                    if mod.ligand:
                        ligand_addtion(f,(c,R,t),mod,ligand_stack)
                elif Structure[i][1] =="0":
                    segment_stack[Structure[i][2:]].append(last_build)
                    if mod.ligand:
                        ligand_addtion(f,(c,R,t),mod,ligand_stack)
            elif Structure[i] == Helix.symbol:
                mod = module_libary[Structure[i]]
                c,R,t = umeyama(module_libary[Structure[i]].start_cord,build[mapping[residue_count-1]])
                for res_index,residue in enumerate(mod.build_cords):
                    atom_count, aligned_sugar = align_base_to_backbonde(f,mod.coord_dict,res_index,seq_index,seq,atom_count,(c,R,t),residue_count)
                    build[residue_count-1] = aligned_sugar
                    last_build = aligned_sugar
                    #print(seq_index,seq[seq_index],residue_count)
                    residue_count += 1
                    seq_index += 1
                    
            else:
                mod = module_libary[Structure[i]]
                c,R,t = umeyama(module_libary[Structure[i]].start_cord,last_build)
                if mod.have_seq:
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
                else:
                    for res_index,residue in enumerate(mod.build_cords):
                        atom_count, aligned_sugar = align_base_to_backbonde(f,mod.coord_dict,res_index,seq_index,seq,atom_count,(c,R,t),residue_count)
                        build[residue_count-1] = aligned_sugar
                        last_build = aligned_sugar
                        #print(seq_index,seq[seq_index],residue_count)
                        residue_count += 1
                        seq_index += 1
                if mod.ligand:
                    ligand_addtion(f,(c,R,t),mod,ligand_stack)

                # keep the module end point for later alignment too
                build[residue_count-1] = last_build
        ligand_printer(f,ligand_stack,atom_count,seq)
            
if __name__ == "__main__":
    
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
