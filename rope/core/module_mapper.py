from rope.core.grid_mapping import generate_np_pattern, map_structure
#from rope.definitions.modules import module_libary, Helix, base
from rope.core.trace_logic import trace_backbone
from rope.definitions.rope_def import one_letter_code, structural_markers
from rope.model.Module import segmented_module
from rope.model.range_dict import RangeDict
from rope.model.records import IndexEntry
from numpy import ndarray




def sequence_matcher(module_seq: str, seq: str) -> bool:
    #print(f"matching {module_seq} to {seq}")
    if len(module_seq) != len(seq):
        return False
    for i in range(len(module_seq)):
        if seq[i] in structural_markers and module_seq[i] in structural_markers:
            if seq[i] != module_seq[i]:
                return False
            continue
        elif seq[i] not in structural_markers and module_seq[i] in structural_markers:
            return False
        elif seq[i] in one_letter_code[module_seq[i]]:
            continue
        elif module_seq[i] != seq[i]:
            return False
    return True

def module_mapper(
    pattern: ndarray | str, index_library: dict[str, IndexEntry]
) -> list[str]:
    """Map a blueprint grid or path to module symbols in traced order.

    The result begins with ``"S"`` for the 5′ end. Indexed modules are tried
    in descending priority/length order and matched against bases and
    structure; segmented modules are accepted only when their paired
    segments are present. Uncovered positions fall back to ``H1``, with
    paired fallback residues represented by ``H2``. Diagnostic messages
    from segmented-module matching are written to standard output.

    Args:
        pattern: Blueprint character grid or path string.
        index_library: Module metadata keyed by module symbol.
    Returns:
        One module symbol for each traced sequence position, with the first
        position labeled ``"S"``.
    """
    if isinstance(pattern, str):
        pattern = generate_np_pattern(pattern)
        
    seq, clean_struc, _, _ = trace_backbone(pattern,crossover = True,header=False)
    mapping = map_structure(clean_struc)
    length = len(seq)
    covered = RangeDict()
    
    base = index_library["H1"]
    helix = index_library["H2"]


    modules = sorted(
        index_library.values(),
        key=lambda x: (x.priority, x.len),
        reverse=True)
    
    for module in modules:
        #print(f"testing for {module.name}")
        if not module.sequence:
            continue
        for seq_index in range(length):
            #print(module.name,module.sequence,seq[seq_index:seq_index+len(module.sequence)])
            if sequence_matcher(module.sequence,seq[seq_index:seq_index+len(module.sequence)]) and seq_index not in covered:
                if module.has_constrain: # tetraloop detection
                    for constrain in module.constrains:
                        if clean_struc[seq_index:seq_index + len(module.sequence)] == constrain:
                            covered[range(seq_index, seq_index + len(module.sequence))] = module.symbol
                    continue
                covered[range(seq_index, seq_index + len(module.sequence))] = module.symbol
            elif module.type == segmented_module: #segment detection
                for segment in module.segments:
                    if module.has_constrain:
                        for constrain in module.constrains:
                            if clean_struc[seq_index:seq_index + len(segment)] == constrain:
                                print(f"segment match {module.name} {segment} {seq[seq_index:seq_index+len(segment)]}")
                    if sequence_matcher(segment, seq[seq_index:seq_index+len(segment)]) and seq_index not in covered:
                        covered[range(seq_index, seq_index + len(segment))] = f"{module.segments.index(segment)}{module.symbol}"
                           

    ###
    #logic for check if both half of a segmented module are present in the strucutre remove any unmatched detections
    ##
    stack = []
    range_stack = []
    istack = []
    irange_stack = []
    for key in covered:
        if len(key) == 1:
            continue
        if covered[key][0] == "0":
            stack.append(covered[key][1:])
            range_stack.append(key)
        if covered[key][0] == "1":
            istack.append(covered[key][1:])
            irange_stack.append(key)
    
    
    index = 0
    while index < len(stack):
        key = stack[index]
        #print(stack,istack,key)
        if key in istack:
            index_stack =  stack.index(key)
            index_istack = istack.index(key)
            stack.pop(index_stack)
            istack.pop(index_istack)
            range_stack.pop(index_stack)
            irange_stack.pop(index_istack)
        else:
            index += 1

    while index < len(istack):
            key = istack[index]
            #print(stack,istack,key)
            if key in stack:
                index_stack =  stack.index(key)
                index_istack = istack.index(key)
                stack.pop(index_stack)
                istack.pop(index_istack)
                range_stack.pop(index_stack)
                irange_stack.pop(index_istack)
            else:
                index += 1
    #print(stack,istack,key)
    #print(range_stack,irange_stack)
    #print(covered)


    range_stack.extend(irange_stack)
    for i in range_stack:
            covered.override(i, base.symbol)
    for i in range(length): # filling out missing elements
            if i > mapping[i] and mapping[i] != -1 and i not in covered and covered[mapping[i]]==base.symbol:
                covered[i] = helix.symbol
            elif i not in covered:
                covered[i] = base.symbol
    #print(range_stack)


    

    #print()
    #print(covered)
    #print()
    
    map_list = []
    covered_list = sorted(covered.items(), key=lambda x: x[0].start if isinstance(x[0], range) else x[0])
    for i in covered_list:
        if covered[i[0]] == base.symbol:
            for j in i[0]:
                map_list.append(base.symbol)
            continue
        map_list.append(covered[i[0]])
    map_list[0]="S"
    
    
    
    ### Logic for labeling of invereted segments
    element_stack = {}
    for i,element in enumerate(map_list):
        if element[0] in ["H","S","T","K","X"]:
            continue
        if element[1:] not in element_stack:
            element_stack[element[1:]] = ([],[])
        #print(element,element_stack)
        if element[0] == "0":
            if element_stack[element[1:]][1] == []:
                element_stack[element[1:]][0].append(i)
            else:
                pair = element_stack[element[1:]][1].pop()
                map_list[pair] = "i0" + map_list[pair][1:]
                map_list[i] = "i1" + map_list[i][1:]
        elif element[0] == "1":
            if element_stack[element[1:]][0] == []:
                element_stack[element[1:]][1].append(i)
            else:
                pair = element_stack[element[1:]][0].pop()
    ##print("stack",element_stack)
        
    print(map_list)
    return map_list
