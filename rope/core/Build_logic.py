from io import TextIOWrapper
from numpy import ndarray, float32
from rope.utils.dim3_utils import umeyama
from rope.model.Module import get_sugar_cords, Module, segmented_module, inv_segmented_module
from rope.definitions.nucleotide import nucleotide_libary
from rope.core.trace_logic import trace_backbone
from rope.core.grid_mapping import generate_np_pattern, map_structure
from rope.core.module_mapper import module_mapper
from rope.io.pdb_io import output_pdb, output_ligand_pdb, get_remarks
from rope.model.ModuleCache import ModuleCache
from rope.model.records import BuildState

def align_base_to_backbonde(buildstate:BuildState,coord_dict:list[dict[int,ndarray]],res_index:int,aligment_variable:tuple[float32,ndarray,ndarray]) -> None:
    c,R,t=aligment_variable
    sugar_residue = get_sugar_cords(coord_dict[res_index])
    aligned_sugar = sugar_residue.dot(c*R)+t
    current_res =buildstate.seq[buildstate.seq_index]
    c2,R2,t2 = umeyama(nucleotide_libary[current_res].start_cord,aligned_sugar)
    align_residue = nucleotide_libary[current_res].build_cords[0].dot(c2*R2)+t2
    for line_index,line in enumerate(nucleotide_libary[current_res].build_lines[0]):
        output_pdb(line,line_index,align_residue,buildstate)
        buildstate.atom_count += 1
    buildstate.build[buildstate.residue_count-1] = aligned_sugar
    buildstate.last_build = aligned_sugar

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

def length_test(Structure:list,seq:str,cache:ModuleCache,ligands):
    Structure_len = 1
    try:
        for i in range(1,len(Structure)):
            if Structure[i][0].isnumeric():
                Structure_len += len(cache.get_module(Structure[i][1:],ligands).segments[int(Structure[i][0])])
                continue
            if Structure[i][0] == "i":
                Structure_len += len(cache.get_module(Structure[i][2:],ligands).segments[int(Structure[i][1])])
                continue
            Structure_len += cache.get_module(Structure[i],ligands).len
        assert Structure_len == len(seq)
    except AssertionError:
        print("Error: The length of the structure and sequence must be the same.")
        print(f"Length of structure: {Structure_len}, Length of sequence: {len(seq)}")
        exit(1)

def build_start(buildstate:BuildState) -> None:
    current_seq = buildstate.seq[buildstate.seq_index]
    for line in nucleotide_libary[current_seq].build_lines[0]:
        buildstate.output.write("".join(line))
        buildstate.atom_count+=1
    last_build = nucleotide_libary[current_seq].start_cord
    buildstate.build[buildstate.residue_count-1]=(last_build)
    buildstate.residue_count+=1
    buildstate.seq_index += 1
    buildstate.last_build = last_build

def build_non_seq_module(buildstate:BuildState,mod:Module,align_var:tuple[float32,ndarray,ndarray]) -> None:
    for res_index,residue in enumerate(mod.build_cords):
        align_base_to_backbonde(buildstate,mod.coord_dict,res_index,align_var)
        #print(seq_index,seq[seq_index],residue_count)
        buildstate.residue_count += 1
        buildstate.seq_index += 1

def build_seq_module(buildstate:BuildState,mod:Module,align_value:tuple[float32,ndarray,ndarray]) -> None:
    c,R,t = align_value
    assert type(mod.sequence) is str
    for res_index,residue in enumerate(mod.build_cords):
        aligned_sugar = get_sugar_cords(mod.coord_dict[res_index]).dot(c*R)+t
        align_residue = residue.dot(c*R)+t
        if mod.sequence[res_index] == "N":
            align_base_to_backbonde(buildstate,mod.coord_dict,res_index,(c,R,t))
        else:
            for line_index,line in enumerate(mod.build_lines[res_index]):
                output_pdb(line,line_index,align_residue,buildstate)
                buildstate.atom_count += 1
        buildstate.build[buildstate.residue_count-1] = aligned_sugar
        buildstate.last_build = aligned_sugar
        buildstate.residue_count += 1
        buildstate.seq_index += 1




def RNAbuild(file:str,output:str,cahce: ModuleCache,index_library,ligands:dict[str,str]|None=None) -> None:
    pattern=generate_np_pattern(file)
    seq,base_pairs,_,_ = trace_backbone(pattern,header=False)
    mapping = map_structure(base_pairs)
    Structure:list = module_mapper(pattern,index_library)

    mod:Module|segmented_module|inv_segmented_module    
    Helix = cahce.get_module("H2",ligands)
    ligand_stack = []
    segment_stack={}
    with open(output, "w") as f:
        buildstate = BuildState(
            build = [ndarray((0,0))]*(len(seq)+1),
            last_build = ndarray((0,0)),
            seq=seq,
            output = f,
            )
        if ligands is not None:
            remarks = get_remarks(file,ligands)
            for remark in remarks:
                f.write(remark)
        for i in range(len(Structure)):
            if Structure[i] == "S":
                build_start(buildstate)

            elif Structure[i][0].isnumeric() or Structure[i][0]=="i":
                if Structure[i][0].isnumeric():
                    mod = cahce.get_module(Structure[i][1:],ligands)
                    offset = 0
                else:
                    mod = cahce.get_module(Structure[i][2:],ligands).inverted()
                    offset = 1
                
                seg_index = int(Structure[i][0+offset])
                if Structure[i][0+offset] == "0":
                    last = buildstate.last_build
                    if Structure[i][1+offset:] not in segment_stack:
                        segment_stack[Structure[i][1+offset:]] = []
                elif Structure[i][0+offset] == "1":
                    last = segment_stack[Structure[i][1+offset:]].pop(-1)
                else:
                    raise Exception



                assert type(mod) == inv_segmented_module or type(mod) == segmented_module
                mod.change_elements(seg_index)
                c,R,t = umeyama(mod.start_cord,last)
                build_seq_module(buildstate,mod,(c,R,t))
                mod.reset_elements()

                if Structure[i][0+offset] == "0":
                    segment_stack[Structure[i][1+offset:]].append(buildstate.last_build)
                    if mod.ligand:
                        ligand_stack = ligand_addtion((c,R,t),mod,ligand_stack)
                elif Structure[i][1] =="0":
                    segment_stack[Structure[i][2:]].append(buildstate.last_build)
                    if mod.ligand:
                        ligand_stack = ligand_addtion((c,R,t),mod,ligand_stack)
            elif Structure[i] == Helix.symbol:
                mod = cahce.get_module(Structure[i],ligands)
                last = buildstate.build[mapping[buildstate.residue_count-1]]
                c,R,t = umeyama(mod.start_cord,last)
                build_non_seq_module(buildstate,mod,(c,R,t))
            else:
                mod = cahce.get_module(Structure[i],ligands)
                c,R,t = umeyama(mod.start_cord,buildstate.last_build)
                if not mod.nonstandard:
                    build_seq_module(buildstate,mod,(c,R,t))
                else:
                    build_non_seq_module(buildstate,mod,(c,R,t))
                if mod.ligand:
                    ligand_stack =ligand_addtion((c,R,t),mod,ligand_stack)

        ligand_printer(f,ligand_stack,buildstate.atom_count,seq)

