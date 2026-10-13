
import argparse
from pathlib import Path
from rope.utils.cli_helper import WideFormatter
import sys
from rope.core.grid_mapping import generate_np_pattern
from rope.utils.temp_files import cleanup_temp_files, make_temp_files
from rope.core.trace_logic import trace_seq_into_backbone, trace_backbone
from rope.io.blueprint_reader import parse_header
from rope.core.revolvr import revolver,KLHandler, compute_ED, dir_mutate_mask_gen
from rope.io.structure_printers import save_multimer_output
from rope.core.analysis_logic import trace_analysis_out
from rope.utils.kl_sample_gen import load_compatibility_file, generate_kl_sample
from rope.definitions.rope_def import kl_meta_list
import RNA
import random
from itertools import product
from copy import deepcopy





def multimer_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
    description="Make multiple blueprints that interact with each other",
    prog="rope-multimer",
    formatter_class=WideFormatter
    )

    parser.add_argument(
        "file",
        metavar="input file",
        help="Input blueprint file"
    )

    parser.add_argument(
        "-r",
        nargs="?",
        default=1,
        metavar="Runs",
        help="Number of runs per input file"
    )

    return parser


def kl_check_bypass (clean_struc:str,init_struc:str,seq:str,init_seq:str,mask:list,ps:int) -> tuple[str,str]:
    return seq, RNA.fold(seq)[0]

def multimer_revolver(temp_files:list[str],kl_handler:KLHandler=kl_check_bypass) -> tuple[str,str,float,float,float,str,str]:
    """Run revolver on a multimer blueprint file with a specified KL handler."""
    meta_kl_pattern = []
    
    
    patterns = []
    traces = []
    for temp_file in temp_files:
        pattern = generate_np_pattern(temp_file)
        patterns.append(pattern)
        head = parse_header(temp_file)[1]
        meta_kl_pattern.append(head)
        traces.append(trace_backbone(pattern,header=head)[1])
    pure_trace = deepcopy(traces)
    meta_index = 0
    kl_chr = 65
    kl = False
    stack = []
   
    kls_in_trace = []
    for j, trace in enumerate(traces):
        trace_list = list(trace)
        kl_id = []
        kl_stack = []
        meta_id = []
        metastart = 0
        for i, char in enumerate(trace_list):
            if char == "@":
                trace_list[i] = str(meta_index)
                kl = True
                metastart = i
            if char != "@" and kl:
                kl =  False
                meta_index += 1
                meta_id.append((metastart,i-1))
            elif trace[i:i+9] == "..[[[[[[.":
                trace_list[i+2:i+8] = [chr(kl_chr)]*6
                stack.append(chr(kl_chr))
                kl_chr += 1
                kl_stack.append((i+2,i+8))
            elif trace[i:i+9] == "..]]]]]].":
                char = stack.pop()
                trace_list[i+2:i+8] = [char]*6
                kl_id.append((kl_stack.pop(),(i+2,i+8)))
        kls_in_trace.append((kl_id,meta_id))
        traces[j] = "".join(trace_list)


    meta_kl_number = 0
    kl_index = 0
    for i in kls_in_trace:
        kl_index += len(i[0])
        meta_kl_number += len(i[1])
    kl_number = meta_kl_number//2 + kl_index
    sample_match = []*len(traces)
    compat,kl_lookup = load_compatibility_file()
    sample = generate_kl_sample(kl_number,compat)

    
    
    sample = generate_kl_sample(kl_number,compat)
    res = [ele for ele in product(sample, repeat = kl_number)]

    need_remove = []
    for i, ele in enumerate(res):
        if len(set(ele)) != len(ele):
            need_remove.append(i)
    for i in need_remove[::-1]:
        res.pop(i)


    init_resualts = []
    for j, file in enumerate(temp_files):        
        init_resualts.append(revolver(file, kl_handler=kl_handler)) ## seq, struc,mfe,feq,min_ed,problem,init_seq

    meta_string = "".join(meta_kl_pattern)


    seq = []
    for j in range(len(init_resualts)):
        seq.append(list(init_resualts[j][0]))

    
    best_score = float("inf")
    best_seqs = []
    


    for i in range(len(res)):
        meta_used = 0
        kl_used = 0
        meta_dict = {}
        normal_dict = {}
        test_seqs = []
        test_eds = []
        test_feq =[]
        for j, trace in enumerate(traces):
            trace_list = list(trace)
            seq_list = seq[j]
            for index in range(len(trace_list)):
                
                if "".join(trace_list[index:index+6]).isalpha():
                    if trace_list[index] in normal_dict:
                        seq_list[index:index+6] = list(kl_lookup[normal_dict[trace_list[index]]][1][3:9])
                        
                    else:
                        used_kl =  res[i][meta_kl_number//2+kl_used]
                        normal_dict[trace_list[index]] = used_kl
                        seq_list[index:index+6] = list(kl_lookup[used_kl][0][3:9])
                       
                
                elif "".join(trace_list[index:index+6]).isnumeric():
                    meta_index_number = int(trace_list[index])
                    meta_identity = meta_string[meta_index_number]
                    if meta_identity in meta_dict:
                        seq_list[index:index+6] = list(kl_lookup[meta_dict[meta_identity]][1][3:9])
                        
                    else:
                        meta_dict[kl_meta_list[meta_identity]] = res[i][meta_used]
                        seq_list[index:index+6] = list(kl_lookup[res[i][meta_used]][0][3:9])
                        
                        meta_used += 1
            test_seqs.append("".join(seq_list))
            mfe,ed,feq = compute_ED("".join(seq_list))
            test_eds.append(ed)
            test_feq.append(feq)
        score = 0
        for j in range(len(test_seqs)):
            score += 1/test_feq[j]*test_eds[j]
        if score < best_score:
            best_score = score
            best_seqs = deepcopy(test_seqs)


            




    multimer_seq = []
    multimer_struc = []
    multimer_mfe = []
    multimer_feq = []
    multimer_ed = []
    multimer_problem = []
    multimer_init_seq = []
    for i, resualt in enumerate(init_resualts):
        seq_string = "".join(best_seqs[i])
        mfe,feq,ed = compute_ED(seq_string)
        struc, mfe = RNA.fold(seq_string)

        ## seq, struc,mfe,feq,min_ed,problem,init_seq
        
        clean_struct = pure_trace[i].replace("[",".").replace("{",".").replace("}",".").replace("]",".")
        problem = dir_mutate_mask_gen(clean_struct,struc,seq_string)

        multimer_seq.append(seq_string)
        multimer_struc.append(struc)
        multimer_mfe.append(mfe)
        multimer_feq.append(feq)
        multimer_ed.append(ed)
        multimer_problem.append(problem)
        multimer_init_seq.append(resualt[-1])

    


    return multimer_seq, multimer_struc, multimer_mfe, multimer_feq, multimer_ed, multimer_problem, multimer_init_seq


def multimer_run_revolver_task(task: tuple[str, int, str,int]) -> None:
    blueprints = []
    blueprint_name = []
    index = -1
    file = task[0]
    run_index = task[1]
    folder = task[2]
    id = task[3]
    with open(file) as f:
        for line in f:
            if line.startswith(">"):
                blueprints.append([])
                blueprint_name.append(line.strip(">").strip())
                index += 1
            
            else:
                blueprints[index].append(line)

    temp_files = make_temp_files(blueprints, blueprint_name)

    patterns = []
    for temp_file in temp_files:
        pattern = generate_np_pattern(temp_file)
        patterns.append(pattern)

            
    multimer_seq, multimer_struc, multimer_mfe, multimer_feq, multimer_ed, multimer_problem, multimer_init_seq = multimer_revolver(temp_files, kl_handler=kl_check_bypass)
    for i in range(len(patterns)):
        new_pattern = trace_seq_into_backbone(multimer_seq[i], str(temp_files[i]))
        analysis_values = trace_analysis_out(None, None, out=False, input_grid=new_pattern)
        assert analysis_values is not None
        save_multimer_output(
            output_dir=Path(f"multimer_output/id_{id}/run_{run_index}"),
            run_index=run_index,
            input_file=str(temp_files[i]),
            seq=multimer_seq[i],
            struc=multimer_struc[i],
            mfe=multimer_mfe[i],
            feq=multimer_feq[i],
            ed=multimer_ed[i],
            problem_mask=multimer_problem[i],
            init_seq=multimer_init_seq[i],
            analysis_values=analysis_values
        )
    cleanup_temp_files(temp_files)

def main():
    args = multimer_parser().parse_args(sys.argv[1:])
    id = random.getrandbits(4)
    for i in range(int(args.r)):
        multimer_run_revolver_task((args.file, i, "multimer_output",id))
    






if __name__ == "__main__":
      main()