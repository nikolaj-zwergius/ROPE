import sys
import os
from pathlib import Path
import concurrent.futures
import rope.core.revolvr as revolvr
import rope.core.trace_logic as trace_logic
from rope.core.analysis_logic import trace_analysis_out
from rope.io.structure_printers import save_revolver_output
from rope.utils.parser_herlper import WideFormatter
import argparse

def batch_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
    prog="rope-fold",
    description="Batch sequnce prediction from blueprint",
    formatter_class=WideFormatter
    )
    
    parser.add_argument(
        "file",
        nargs="?",
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


    return parser

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
    wd = os.getcwd()
    out_folder = Path(wd+"/revolver_outputs")

    args = batch_parser().parse_args(sys.argv[1:])
    file_args = []
    runs = 1
    max_workers = None
    if args.w:
        max_workers = int(args.w)
    if args.r:
        runs = int(args.r)
    if args.file is None or args.file == "*":
        for file in os.listdir():
            if not file.endswith(".txt"):
                continue
            else:
                file_args.append(file)
        args.file = file_args
    print("starting")
    run_revolvers(args.file, runs_per_file=runs, max_workers=max_workers,output_root=out_folder)

    
if __name__ == "__main__":
    main()