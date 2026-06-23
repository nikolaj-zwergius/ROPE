import sys
import os
from pathlib import Path
import concurrent.futures
import revolvr
import trace_pattern
import trace_analysis as ta
from utils.rope_def import VALID_BASES
import utils.trace_utils as tu
from utils.render_utils import structure_printer, render_pattern


def save_revolver_output(output_dir: Path, run_index: int, input_file: str, seq: str, struc: str, mfe: float, feq: float, ed: float,problem_mask:list,init_seq:str) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    ed_str = f"{ed:.2f}"
    output_path = output_dir / f"{ed_str}_run_{run_index:03d}.txt"
    new_pattern = trace_pattern.trace_seq_into_backbone(seq, input_file)
    grid, seq_output, repeat_map, wobbles_seq, barriers, complement_zones, duplicate_zones, pattern_repeats, poly_repeats, restriction_sites, n_map, strand_dir = ta.trace_analysis_out(None, None, out=False, input_grid=new_pattern)
    with output_path.open("w", encoding="utf-8") as out_file:
        out_file.write(f"input_file: {input_file}\n")
        out_file.write(f"run_index: {run_index}\n")
        out_file.write(f"sequence: {seq}\n")
        out_file.write(f"structure: {struc}\n")
        out_file.write(f"mfe: {mfe:.2f}\n")
        out_file.write(f"feq: {feq:.2f}\n")
        out_file.write(f"ed: {ed:.2f}\n")
        gc = revolvr.gc_ratio_calculator(seq)
        if gc > 51: out_file.write(f"GC: {gc:.2f} WARNING: GC content above the maximum of 51 from ROAD \n")
        else:out_file.write(f"GC: {gc:.2f}\n")
        out_file.write("\n\n\n")
        if revolvr.problem_in_loced(problem_mask,init_seq,control=False):
            out_file.write("""\tWARNING: Misfolding within the locked-sequence required altering the target structure 
             Sequence design failed for the inputted target structure.\n""")
            render_pattern(out_file,"\n\nHighlighting changed structural regions\n",problem_mask,n_map,grid)
            out_file.write("\n")
        structure_printer(out_file,grid, seq_output, repeat_map, wobbles_seq, barriers, complement_zones, duplicate_zones, pattern_repeats, poly_repeats, restriction_sites, n_map, strand_dir,problem_mask)
        

def _run_dragon_task(task: tuple[str, int, str,int]) -> None:
    file_path, run_index, output_root,target_ed = task
    input_path = Path(file_path)
    output_dir = Path(output_root) / input_path.stem / Path(f"run_{run_index}")
    ed = float("inf")
    output_dir.mkdir(parents=True, exist_ok=True)
    grid = tu.generate_np_pattern(file_path)
    seq,_,_,_ = trace_pattern.trace_backbone(grid)
    one_run = False
    if set(seq) ==  set(VALID_BASES):
        one_run = True
    while ed > target_ed:
        seq, struc, mfe, feq, ed, problem,init_seq = revolvr.revolver(str(input_path))
        if len(os.listdir(output_dir)) == 0:
            save_revolver_output(output_dir, run_index, str(input_path), seq, struc, mfe, feq, ed, problem,init_seq)
            continue
        if ed < float(os.listdir(output_dir)[0][:3]):
            save_revolver_output(output_dir, run_index, str(input_path), seq, struc, mfe, feq, ed, problem,init_seq)
        if one_run:
            return


def run_dragons(files: list[str], runs_per_file: int = 1, output_root: str = "revolver_outputs", max_workers: int|None = None,target_ed=0) -> None:
    """Run revolver on each input file multiple times in parallel and save outputs in per-file folders."""
    root_dir = Path(output_root)
    root_dir.mkdir(parents=True, exist_ok=True)
    tasks = []
    for file_path in files:
        input_path = Path(file_path)
        if not input_path.is_file():
            raise FileNotFoundError(f"Input file not found: {input_path}")
        for run_index in range(1, runs_per_file + 1):
            tasks.append((str(input_path), run_index, str(root_dir),target_ed))

    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        for _ in executor.map(_run_dragon_task, tasks):
            pass


if __name__ == "__main__":
    dir_path = os.path.dirname(os.path.realpath(__file__))  
    parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
    wd = os.getcwd()
    out_folder = Path(wd+"/dragon_outputs")

    args = sys.argv[1:]
    file_args = []
    runs = 1
    max_workers = 1
    target_ed=0
    if args and args[-1].isdigit():
      target_ed = int(args[-1])
      args = args[:-1]
    if args and args[-1].isdigit():
      runs = int(args[-1])
      args = args[:-1]
    if args and args[-1].isdigit():
        max_workers = int(args[-1])
        args = args[:-1]
    if not args or args[-1] == "*":
         for file in os.listdir():
            if not file.endswith(".txt"):
                continue
            else:
                file_args.append(file)
    args.extend(file_args)
    if max_workers == 1 and runs ==1:
        max_workers = len(args)
    if runs*len(args) > max_workers:
        print("Dragon will not work with less tasks then workers")
        exit()
    run_dragons(args, runs_per_file=runs, max_workers=max_workers,output_root=out_folder,target_ed=target_ed)
