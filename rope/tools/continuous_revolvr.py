
import sys
from pathlib import Path
import os
import concurrent.futures
import rope.core.revolvr as revolvr
import rope.core.trace_logic as trace_logic
from rope.core.analysis_logic import trace_analysis_out
from rope.definitions.rope_def import VALID_BASES
import rope.core.grid_mapping as tu
from rope.io.structure_printers import save_revolver_output
import argparse
from rope.utils.parser_herlper import WideFormatter
import time

def continuous_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
    description="Continuous sequnce predection from blueprint",
    prog="rope-dragon",
    formatter_class=WideFormatter
    )
    
    parser.add_argument(
        "file",
        nargs="*",
        metavar="input file",
        help="Input file if none given all valid files in folder will be processed"
    )

    parser.add_argument(
        "-r",
        nargs="?",
        const=1,
        metavar="Runs",
        help="Number of runs per input file"
    )

    parser.add_argument(
        "-w",
        nargs="?",
        const= 1,
        metavar="Workers/Theads",
        help="Number of workers/theads assigned to the job"
    )

    parser.add_argument(
        "-e",
        nargs="?",
        const= 1,
        metavar="ED",
        help="Target Ensemble diversity"
    )
    parser.add_argument(
        "-t",
        nargs="?",
        const= 0,
        metavar="Time per run",
        help="Maximum time per run, in the format xd:xh:xm:xs "
    )


    return parser        

def _run_dragon_task(task: tuple[str, int, str,int,int]) -> None:
    file_path, run_index, output_root,target_ed,timer = task
    input_path = Path(file_path)
    output_dir = Path(output_root) / input_path.stem / Path(f"run_{run_index}")
    ed = float("inf")
    output_dir.mkdir(parents=True, exist_ok=True)
    grid = tu.generate_np_pattern(file_path)
    seq,_,_,_ = trace_logic.trace_backbone(grid,header=False)
    one_run = False
    if set(seq) ==  set(VALID_BASES) and "N" not in set(seq):
        one_run = True
    start = time.time()
    time_since_start = 0
    while ed > target_ed and (timer >= time_since_start or  timer == 0):
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
        time_since_start = time.time() - start
        


def run_dragons(files: list[str], runs_per_file: int = 1, output_root: str|Path = "revolver_outputs", max_workers: int|None = None,target_ed=0,timer=0) -> None:
    """Run revolver on each input file multiple times in parallel and save outputs in per-file folders."""
    root_dir = Path(output_root)
    root_dir.mkdir(parents=True, exist_ok=True)
    tasks = []
    for file_path in files:
        input_path = Path(file_path)
        if not input_path.is_file():
            raise FileNotFoundError(f"Input file not found: {input_path}")
        for run_index in range(1, runs_per_file + 1):
            tasks.append((str(input_path), run_index, str(root_dir),target_ed,timer))

    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        for _ in executor.map(_run_dragon_task, tasks):
            pass

def main():
    wd = os.getcwd()
    out_folder = Path(wd+"/dragon_outputs")

    args = continuous_parser().parse_args(sys.argv[1:])
    file_args = []
    runs = 1
    max_workers = 1
    target_ed=0
    if args.r:
      runs = int(args.r)
    if args.w:
        max_workers = int(args.w)
    if args and args.e:
      target_ed = int(args.e)
    if args.file == [] or args.file == "*":
        for file in os.listdir():
            if not file.endswith(".txt"):
                continue
            else:
                file_args.append(file)
        args.file = file_args
    if max_workers == 1 and runs ==1:
        max_workers = len(args.file)
    if runs*len(args.file) > max_workers:
        print("Dragon will not work with less tasks then workers")
        exit()
    max_time_int = 0
    if args.t:
        max_time = args.t
        max_time_list:list[str] = max_time.split(":")
        for elem in max_time_list:
            if elem.lower().endswith("d"):
                max_time_int += int(elem.strip("d").strip("D"))*86400
            if elem.lower().endswith("h"):
                max_time_int += int(elem.strip("h").strip("H"))*3600
            if elem.lower().endswith("m"):
                max_time_int += int(elem.strip("m").strip("M"))*60
            if elem.lower().endswith("s"):
                max_time_int += int(elem.strip("s").strip("S"))
            if elem.isnumeric():
                raise TypeError("values need to be followed be a timescale indicator d(days) h(hours) m(miniuts) s(seconds)")
    run_dragons(args.file, runs_per_file=runs, max_workers=max_workers,output_root=out_folder,target_ed=target_ed,timer=max_time_int)

if __name__ == "__main__":
    main()
