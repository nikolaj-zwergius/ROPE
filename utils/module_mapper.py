
from revolvr import base_pair_mapper
from utils.trace_utils import generate_np_pattern
from utils.modules import module_libary
from trace_pattern import trace_backbone
from utils.rope_def import one_letter_code
from utils.def_class import segmented_module, RangeDict




def sequnce_matcher(module_seq,seq):
    
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

def module_mapper(pattern):
    """Map a traced RNA sequence to a list of module symbols.

    The returned list begins with "S" for the 5' end, then includes module symbols
    in sequence order. Known module sequences are matched greedily, and any
    uncovered residue is filled with a helix module "H".
    """
    if isinstance(pattern, str):
        pattern = generate_np_pattern(pattern)

    seq, clean_struc, _, _ = trace_backbone(pattern,crossover = True)

    length = len(seq)
    covered = RangeDict()

    modules = sorted(module_libary.values(), reverse=True)
    for module in modules:
        for seq_index in range(length):
            if module.sequence is None:
                continue
            if sequnce_matcher(module.sequence,seq[seq_index:seq_index+len(module.sequence)]) and seq_index not in covered:
                covered[range(seq_index, seq_index + len(module.sequence))] = module.symbol
            elif isinstance(module, segmented_module):
                for segment in module.segments:
                    if sequnce_matcher(segment, seq[seq_index:seq_index+len(segment)]) and seq_index not in covered:
                        covered[range(seq_index, seq_index + len(segment))] = f"{module.segments.index(segment)}{module.symbol}"
    for i in range(length):
        if i not in covered:
            covered[i] = "H"
    
    
    stack = []
    range_stack = []
    for key in covered:
        if len(key) == 1:
            continue
        if covered[key][1:] in stack:
            stack.pop()
            range_stack.pop()
        if covered[key][0] == "0":
            stack.append(covered[key][1:])
            range_stack.append(key)
    for i in range_stack:
        covered.override(i, "H")
    map_list = []
    covered_list = sorted(covered.items(), key=lambda x: x[0].start if isinstance(x[0], range) else x[0])
    for i in covered_list:
        if covered[i[0]] == "H":
            for j in i[0]:
                map_list.append("H")
            continue
        map_list.append(covered[i[0]])
    map_list[0]="S"
    return map_list


