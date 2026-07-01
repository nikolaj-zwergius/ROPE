
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
from rope.io.structure_printers import structure_printer, render_pattern, save_revolver_output
   

def _run_revolver_task(task: tuple[str, int, str]) -> None:
    file_path, run_index, output_root = task
    input_path = Path(file_path)
    output_dir = Path(output_root) / input_path.stem

    seq, struc, mfe, feq, ed, problem,init_seq = revolvr.revolver(str(input_path))
    new_pattern = trace_logic.trace_seq_into_backbone(seq, str(input_path))
    analysis_values = trace_analysis_out(None, None, out=False, input_grid=new_pattern)
    assert analysis_values is not None
    save_revolver_output(output_dir, run_index, str(input_path), seq, struc, mfe, feq, ed, problem,init_seq,analysis_values)


def run_revolvers(files: list[str], runs_per_file: int = 1, output_root: str|Path = "revolver_outputs", max_workers: int|None = None) -> None:
    """Run revolver on each input file multiple times in parallel and save outputs in per-file folders."""
    root_dir = Path(output_root)
    root_dir.mkdir(parents=True, exist_ok=True)
    tasks = []
    for file_path in files:
        input_path = Path(file_path)
        if not input_path.is_file():
            raise FileNotFoundError(f"Input file not found: {input_path}")
        for run_index in range(1, runs_per_file + 1):
            tasks.append((str(input_path), run_index, str(root_dir)))

    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        for _ in executor.map(_run_revolver_task, tasks):
            pass

def main():
    print("starting")
    dir_path = os.path.dirname(os.path.realpath(__file__))  
    parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
    wd = os.getcwd()
    out_folder = Path(wd+"/revolver_outputs")

    args = sys.argv[1:]
    file_args = []
    runs = 1
    max_workers = None
    if args and args[-1].isdigit():
        max_workers = int(args[-1])
        args = args[:-1]
    if args and args[-1].isdigit():
        runs = int(args[-1])
        args = args[:-1]
    if not args or args[-1] == "*":
         for file in os.listdir():
            if not file.endswith(".txt"):
                continue
            else:
                file_args.append(file)
    args.extend(file_args)
    print("starting")
    run_revolvers(args, runs_per_file=runs, max_workers=max_workers,output_root=out_folder)

    
if __name__ == "__main__":
    main()