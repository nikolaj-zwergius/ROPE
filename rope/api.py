
from rope.core.trace_logic import generate_np_pattern,trace_backbone
from rope.utils.dim3_utils import umeyama
from rope.tools.build import RNAbuild

def run_trace(pattern_file:str) -> tuple[str,str]:
    pattern = generate_np_pattern(pattern_file)
    seq,base_pair,_,_= trace_backbone(pattern)
    return seq,base_pair

def run_RNAbuild(blueprint_file:str,output_path:str) -> None:
    RNAbuild(blueprint_file,output_path)

umeyama = umeyama