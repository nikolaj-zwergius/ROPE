import numpy as np
from utils.dim3_utils import align_vectors, umeyama
from utils.def_class import get_sugar_cords, Module, segmented_module
from utils.modules import module_libary, Helix
from utils.nucleotide import nucleotide_libary
from trace_pattern import trace_backbone
from utils.trace_utils import generate_np_pattern, map_structure
from utils.module_mapper import module_mapper
def output_pdb(line,seq,index,line_index,align_residue):
    line_string = list(line)
    line_string[6:11] = f"{atom_count:5d}"
    line_string[17:20] = f"{seq[index]:>3s}"
    line_string[22:26] = f"{residue_count:4d}"
    line_string[30:38] = f"{align_residue[line_index][0]:8.3f}"
    line_string[38:46] = f"{align_residue[line_index][1]:8.3f}"
    line_string[46:54] = f"{align_residue[line_index][2]:8.3f}"
    return "".join(line_string)

def align_base_to_backbonde(f,coord_dict,res_index,seq_index,seq,atom_count):
    sugar_residue = get_sugar_cords(coord_dict[res_index])
    align_sugar = sugar_residue.dot(c*R)+t
    c2,R2,t2 = umeyama(nucleotide_libary[seq[seq_index]].start_cord,align_sugar)
    align_residue = nucleotide_libary[seq[seq_index]].build_cords[0].dot(c2*R2)+t2
    for line_index,line in enumerate(nucleotide_libary[seq[seq_index]].build_lines[0]):
        f.write(output_pdb(line,seq,seq_index,line_index,align_residue))
        atom_count += 1
    return atom_count, align_sugar

pattern=generate_np_pattern("build_test.txt")
seq,base_pairs,_,_ = trace_backbone(pattern)
mapping = map_structure(base_pairs)

Structure:str = module_mapper(pattern)
build = [None]*(len(seq)+1)
print(Structure)
print("K:",Structure.count("K"))
print("T:",Structure.count("T"))
print("X:",Structure.count("X"))
print("H1:",Structure.count("H1"))
print("H2:",Structure.count("H2"))
module = Module
try:
    Structure_len = 1
    for i in range(1,len(Structure)):
        if Structure[i][0].isnumeric():
            Structure_len += len(module_libary[Structure[i][1:]].segments[int(Structure[i][0])])
            continue
        Structure_len += module_libary[Structure[i]].len
    assert Structure_len == len(seq)
except AssertionError:
    print("Error: The length of the structure and sequence must be the same.")
    print(f"Length of structure: {Structure_len}, Length of sequence: {len(seq)}")
    exit(1)



with open("target.pdb", "w") as f:
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
            residue_count+=1
            seq_index += 1

        elif Structure[i][0].isnumeric():
            seg_index = int(Structure[i][0])
            mod:segmented_module = module_libary[Structure[i][1:]]
            c,R,t = umeyama(mod.segment_start_cord[seg_index],last_build)
            for res_index,residue in enumerate(mod.segment_build_cords[seg_index]):
                aligned_sugar = get_sugar_cords(mod.segment_coord_dict[seg_index][res_index]).dot(c*R)+t
                align_residue = residue.dot(c*R)+t
                if mod.segments[seg_index][res_index] == "N":
                    atom_count, aligned_sugar = align_base_to_backbonde(f,mod.segment_coord_dict[seg_index],res_index,seq_index,seq,atom_count)
                else:    
                    print(len(mod.segment_build_lines[seg_index]))
                    for line_index,line in enumerate(mod.segment_build_lines[seg_index][res_index]):
                        f.write(output_pdb(line,mod.segments[seg_index],res_index,line_index,align_residue))
                        atom_count += 1
                build[residue_count-1] = aligned_sugar
                last_build = aligned_sugar
                residue_count += 1
                seq_index += 1
        elif Structure[i] == Helix.symbol:
            mod = module_libary[Structure[i]]
            c,R,t = umeyama(module_libary[Structure[i]].start_cord,build[mapping[residue_count-1]])
            for res_index,residue in enumerate(mod.build_cords):
                atom_count, aligned_sugar = align_base_to_backbonde(f,mod.coord_dict,res_index,seq_index,seq,atom_count)
                build[residue_count-1] = aligned_sugar
                last_build = aligned_sugar
                seq_index += 1
                residue_count += 1
        else:
            mod = module_libary[Structure[i]]
            c,R,t = umeyama(module_libary[Structure[i]].start_cord,last_build)
            if mod.have_seq:
                for res_index,residue in enumerate(mod.build_cords):
                    
                    aligned_sugar = get_sugar_cords(mod.coord_dict[res_index]).dot(c*R)+t
                    align_residue = residue.dot(c*R)+t
                    if mod.sequence[res_index] == "N":
                        atom_count, aligned_sugar = align_base_to_backbonde(f,mod.coord_dict,res_index,seq_index,seq,atom_count)
                    else:    
                        for line_index,line in enumerate(mod.build_lines[res_index]):
                            f.write(output_pdb(line,mod.sequence,res_index,line_index,align_residue))
                            atom_count += 1
                    build[residue_count-1] = aligned_sugar
                    last_build = aligned_sugar
                    residue_count += 1
                    seq_index += 1
            else:
                for res_index,residue in enumerate(mod.build_cords):
                    atom_count, aligned_sugar = align_base_to_backbonde(f,mod.coord_dict,res_index,seq_index,seq,atom_count)
                    build[residue_count-1] = aligned_sugar
                    last_build = aligned_sugar
                    residue_count += 1
                    seq_index += 1
            # keep the module end point for later alignment too
            build[residue_count-1] = last_build

            
