from rope.core.grid_mapping import generate_np_pattern, map_structure
from rope.definitions.modules import module_libary, Helix, base
from rope.core.trace_logic import trace_backbone
from rope.definitions.rope_def import one_letter_code
from rope.model.Module import segmented_module, RangeDict
from numpy import ndarray



def sequnce_matcher(module_seq:str,seq:str):
    if len(module_seq) != len(seq):
        return False
    for i in range(len(module_seq)):
        if seq[i] == "^" and module_seq[i] == "^":
            continue
        elif seq[i] != "^" and module_seq[i] == "^":
            return False
        elif seq[i] in one_letter_code[module_seq[i]]:
            continue
        elif module_seq[i] != seq[i]:
            return False
    return True

def module_mapper(pattern:ndarray):
    """Map a traced RNA sequence to a list of module symbols.

    The returned list begins with "S" for the 5' end, then includes module symbols
    in sequence order. Known module sequences are matched greedily, and any
    uncovered residue is filled with a unpaired helix module "H1".
    """
    if isinstance(pattern, str):
        pattern = generate_np_pattern(pattern)

    seq, clean_struc, _, _ = trace_backbone(pattern,crossover = True)
    mapping = map_structure(clean_struc)
    length = len(seq)
    covered = RangeDict()

    kl_detect = False
    kls = []
    soft_kls = []
    for i in range(len(clean_struc)):
        if (clean_struc[i] == "[" or clean_struc[i] == "]") and not kl_detect:
            kl_detect = True
            kls.append(i)
        if kl_detect and (clean_struc[i] != "[" and clean_struc[i] != "]"):
            kl_detect = False
    for i in range(len(seq)-9):
        if seq[i:i+2] == "AA" and seq[i+8]=="A":
            if clean_struc[i:i+9] == ".........":
                soft_kls.append(i)

    modules = sorted(module_libary.values(), reverse=True)
    for module in modules:
        if module.sequence is None:
            continue
        for seq_index in range(length):
            if module == module_libary["K"]: #Kissing loop labeling
                if seq_index in kls:
                    covered[range(seq_index-4,seq_index+9)] = "K"
                if seq_index in soft_kls:
                    covered[range(seq_index-2,seq_index+11)] = "K"
                continue
            if sequnce_matcher(module.sequence,seq[seq_index:seq_index+len(module.sequence)]) and seq_index not in covered:
                if module == module_libary["T"]: # tetraloop detection
                    if clean_struc[seq_index:seq_index + len(module.sequence)] == "(....)":
                        covered[range(seq_index, seq_index + len(module.sequence))] = module.symbol
                    continue
                covered[range(seq_index, seq_index + len(module.sequence))] = module.symbol
            elif isinstance(module, segmented_module): #segment detection
                for segment in module.segments:
                    if sequnce_matcher(segment, seq[seq_index:seq_index+len(segment)]) and seq_index not in covered:
                        covered[range(seq_index, seq_index + len(segment))] = f"{module.segments.index(segment)}{module.symbol}"
                           
    for i in range(length): # filling out missing elements
        if i > mapping[i] and mapping[i] != -1 and i not in covered and covered[mapping[i]]==base.symbol:
            covered[i] = Helix.symbol
        elif i not in covered:
            covered[i] = base.symbol
    
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
    
    for key in covered:
        if covered[key][1:] in stack and covered[key][0] != "0":
            stack.pop(stack.index(covered[key][1:]))
            range_stack.pop()
        if covered[key][1:] in istack and covered[key][0] != "1":
            istack.pop(istack.index(covered[key][1:]))
            irange_stack.pop()
    range_stack.extend(irange_stack)
    for i in range_stack:
        covered.override(i, base.symbol)
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
    pairs = {}
    for i,element in enumerate(map_list):
        if element[0] in ["H","S","T","K","X"]:
            continue
        if element[0].isnumeric():
            if element[1:] in pairs:
                if int(element[0]) < int(pairs[element[1:]][0]):
                    map_list[pairs[element[1:]][1]] = "i"+element
                    map_list[i] = "i"+pairs[element[1:]][2]
                else:
                    pass
            else:
                pairs[element[1:]] = (element[0],i,element)
    
        

    return map_list
