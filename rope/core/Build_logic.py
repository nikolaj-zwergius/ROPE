from io import TextIOWrapper
from numpy import ndarray, float32
from rope.utils.dim3_utils import umeyama
from rope.model.Module import get_sugar_cords, Module, segmented_module, inv_segmented_module
from rope.definitions.modules import module_libary, Helix
from rope.definitions.nucleotide import nucleotide_libary
from rope.core.trace_logic import trace_backbone
from rope.core.grid_mapping import generate_np_pattern, map_structure
from rope.core.module_mapper import module_mapper
from rope.io.pdb_io import output_pdb, output_ligand_pdb, get_remarks
from rope.io.blueprint_reader import parse_header
from rope.io.index_handler import load_index



def align_base_to_backbonde(f:TextIOWrapper,coord_dict:list[dict[int,ndarray]],res_index:int,seq_index:int,seq:str,atom_count:int,aligment_variable:tuple[float32,ndarray,ndarray],residue_count:int) -> tuple[int,ndarray]:
    c,R,t=aligment_variable
    sugar_residue = get_sugar_cords(coord_dict[res_index])
    align_sugar = sugar_residue.dot(c*R)+t
    c2,R2,t2 = umeyama(nucleotide_libary[seq[seq_index]].start_cord,align_sugar)
    align_residue = nucleotide_libary[seq[seq_index]].build_cords[0].dot(c2*R2)+t2
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
    Structure_len = 1
    try:
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

def build_non_seq_module(f:TextIOWrapper,mod:Module,build:list,align_var:tuple[float32,ndarray,ndarray],seq:str,atom_count:int,residue_count:int,seq_index:int) -> tuple[int,ndarray,list,int,int]:
    last_build = ndarray((0,0))
    for res_index,residue in enumerate(mod.build_cords):
        atom_count, aligned_sugar = align_base_to_backbonde(f,mod.coord_dict,res_index,seq_index,seq,atom_count,align_var,residue_count)
        build[residue_count-1] = aligned_sugar
        last_build = aligned_sugar
        #print(seq_index,seq[seq_index],residue_count)
        residue_count += 1
        seq_index += 1
    return atom_count,last_build,build,residue_count,seq_index

def build_seq_module(f:TextIOWrapper,mod:Module,build:list[ndarray],align_value:tuple[float32,ndarray,ndarray],seq:str,atom_count:int,residue_count:int,seq_index:int) -> tuple[int,ndarray,list,int,int]:
    last_build = ndarray((0,0))
    c,R,t = align_value
    assert type(mod.sequence) is str
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




def RNAbuild(file:str,output:str,ligands:dict[str,str]|None=None) -> None:
    for i in module_libary:
        module_libary[i].reset()
    pattern=generate_np_pattern(file)
    seq,base_pairs,_,_ = trace_backbone(pattern,header=False)
    mapping = map_structure(base_pairs)
    index_library = load_index()
    Structure:list = module_mapper(pattern,index_library)
    build = [ndarray((0,0))]*(len(seq)+1)
    ligand_stack = []
    mod:Module|segmented_module|inv_segmented_module

    segment_stack={}
    last_build = ndarray((0,0))

    with open(output, "w") as f:
        if ligands is not None:
            remarks = get_remarks(file,ligands)
            for remark in remarks:
                f.write(remark)
        atom_count = 1
        residue_count = 1
        seq_index = 0
        for i in range(len(Structure)):
            if Structure[i] == "S":
                atom_count,last_build,build,residue_count,seq_index = build_start(f,seq[i],atom_count,build,residue_count,seq_index)

            elif Structure[i][0].isnumeric() or Structure[i][0]=="i":
                if Structure[i][0].isnumeric():
                    mod = module_libary[Structure[i][1:]]
                    offset = 0
                else:
                    mod = module_libary[Structure[i][2:]].inverted()
                    offset = 1

                seg_index = int(Structure[i][0+offset])

                if Structure[i][0+offset] == "0":
                    last = last_build
                    if Structure[i][1+offset:] not in segment_stack:
                        segment_stack[Structure[i][1+offset:]] = []
                elif Structure[i][0+offset] == "1":
                    last = segment_stack[Structure[i][1+offset:]].pop(-1)
                else:
                    raise Exception



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
                mod = module_libary[Structure[i]]
                build[mapping[residue_count-1]]
                c,R,t = umeyama(mod.start_cord,build[mapping[residue_count-1]])
                atom_count,last_build,build,residue_count,seq_index =build_non_seq_module(f,mod,build,(c,R,t),seq,atom_count,residue_count,seq_index)
            else:
                mod = module_libary[Structure[i]]
                c,R,t = umeyama(module_libary[Structure[i]].start_cord,last_build)
                if not mod.nonstandard:
                    atom_count,last_build,build,residue_count,seq_index = build_seq_module(f,mod,build,(c,R,t),seq,atom_count,residue_count,seq_index)
                else:
                    atom_count,last_build,build,residue_count,seq_index =build_non_seq_module(f,mod,build,(c,R,t),seq,atom_count,residue_count,seq_index)
                if mod.ligand:
                    ligand_stack =ligand_addtion((c,R,t),mod,ligand_stack)

                build[residue_count-1] = last_build
        ligand_printer(f,ligand_stack,atom_count,seq)

