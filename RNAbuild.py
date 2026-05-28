import numpy as np
from utils.dim3_utils import align_vectors, umeyama
from RNA_lib.def_class import get_sugar_cords, Module
from RNA_lib.modules import module_libary
from RNA_lib.nucleotide import nucleotide_libary
def output_pdb(line,seq,index,line_index,align_residue):
    line_string = list(line)
    line_string[6:11] = f"{atom_count:5d}"
    line_string[17:20] = f"{seq[index]:>3s}"
    line_string[22:26] = f"{residue_count:4d}"
    line_string[30:38] = f"{align_residue[line_index][0]:8.3f}"
    line_string[38:46] = f"{align_residue[line_index][1]:8.3f}"
    line_string[46:54] = f"{align_residue[line_index][2]:8.3f}"
    return "".join(line_string)

def align_base_to_backbonde(f,mod,res_index,seq_index,seq,atom_count):
    sugar_residue = get_sugar_cords(mod.coord_dict[res_index])
    align_sugar = sugar_residue.dot(c*R)+t
    c2,R2,t2 = umeyama(nucleotide_libary[seq[seq_index]].start_cord,align_sugar)
    align_residue = nucleotide_libary[seq[seq_index]].build_cords[0].dot(c2*R2)+t2
    for line_index,line in enumerate(nucleotide_libary[seq[seq_index]].build_lines[0]):
        f.write(output_pdb(line,seq,seq_index,line_index,align_residue))
        atom_count+=1 
    return atom_count


Structure = ["S","H","H","H","H","H","H","H","H","H","lT","H","H","H","H","H","H","H","H","H","H","H"]
seq = "AAGCGCGCAAGGUUCGGGGGGCGCGCGCC"
module = Module()
try:
    Structure_len = 1
    for i in range(1,len(Structure)):
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
            residue_count+=1
            seq_index += 1

        elif Structure[i][0].isdigit():
            pass
        else:
            mod = module_libary[Structure[i]]
            c,R,t = umeyama(module_libary[Structure[i]].start_cord,last_build)
            if mod.have_seq:
                for res_index,residue in enumerate(mod.build_cords):
                    align_residue = residue.dot(c*R)+t
                    if mod.sequence[res_index] == "N":
                        atom_count = align_base_to_backbonde(f,mod,res_index,seq_index,seq,atom_count)
                    else:    
                        for line_index,line in enumerate(mod.build_lines[res_index]):
                            f.write(output_pdb(line,mod.sequence,res_index,line_index,align_residue))
                            atom_count+=1
                    residue_count+=1
                    seq_index += 1
            elif mod.have_seq and mod.sequence.count("N") > 0:
                pass
            else:
                 for res_index,residue in enumerate(mod.build_cords):
                    atom_count = align_base_to_backbonde(f,mod,res_index,seq_index,seq,atom_count)
                    residue_count+=1
                    seq_index+=1
            last_build = mod.last_coord.dot(c*R)+t

