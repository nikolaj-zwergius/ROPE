
from core.trace_logic import generate_np_pattern,trace_backbone

def run_trace(pattern_file):
    pattern = generate_np_pattern(pattern_file)
    seq,base_pair,_,_= trace_backbone(pattern)
    return seq,base_pair