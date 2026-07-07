
import sys
from pathlib import Path

# Add project root to Python path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import sys
import os
from pathlib import Path
import concurrent.futures
import rope.core.revolvr as revolvr
import rope.core.trace_logic as trace_logic
from rope.core.analysis_logic import trace_analysis_out
from rope.definitions.rope_def import VALID_BASES
import rope.core.grid_mapping as tu
from rope.io.structure_printers import structure_printer, render_pattern, save_revolver_output

        

def _run_dragon_task(task: tuple[str, int, str,int]) -> None:
    file_path, run_index, output_root,target_ed = task
    input_path = Path(file_path)
    output_dir = Path(output_root) / input_path.stem / Path(f"run_{run_index}")
    ed = float("inf")
    output_dir.mkdir(parents=True, exist_ok=True)
    grid = tu.generate_np_pattern(file_path)
    seq,_,_,_ = trace_logic.trace_backbone(grid)
    one_run = False
    if set(seq) ==  set(VALID_BASES):
        one_run = True
    while ed > target_ed:
        seq, struc, mfe, feq, ed, problem,init_seq = revolvr.revolver(str(input_path))
        new_pattern = trace_logic.trace_seq_into_backbone(seq, str(input_path))
        analysis_values = trace_analysis_out(None, None, out=False, input_grid=new_pattern)
        if len(os.listdir(output_dir)) == 0:
            save_revolver_output(output_dir, run_index, str(input_path), seq, struc, mfe, feq, ed, problem,init_seq,analysis_values)
            continue
        if ed < float(os.listdir(output_dir)[0][:3]):
            save_revolver_output(output_dir, run_index, str(input_path), seq, struc, mfe, feq, ed, problem,init_seq,analysis_values)
        if one_run:
            return


def run_dragons(files: list[str], runs_per_file: int = 1, output_root: str|Path = "revolver_outputs", max_workers: int|None = None,target_ed=0) -> None:
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

def main():
    wd = os.getcwd()
    out_folder = Path(wd+"/dragon_outputs")

    args = sys.argv[1:]
    file_args = []
    runs = 1
    max_workers = 1
    target_ed=0
    if args and args[-1].isdigit():
      runs = int(args[-1])
      args = args[:-1]
    if args and args[-1].isdigit():
        max_workers = int(args[-1])
        args = args[:-1]
    if args and args[-1].isdigit():
      target_ed = int(args[-1])
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

if __name__ == "__main__":
    main()
