
from rope.core.trace_logic import generate_np_pattern,trace_backbone
from rope.utils.dim3_utils import umeyama

def run_trace(pattern_file):
    pattern = generate_np_pattern(pattern_file)
    seq,base_pair,_,_= trace_backbone(pattern)
    return seq,base_pair