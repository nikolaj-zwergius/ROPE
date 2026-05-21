from pathlib import Path
import concurrent.futures
from typing import Optional

import revolvr
import rope_def as rd


def save_revolver_output(output_dir: Path, run_index: int, input_file: str, seq: str, struc: str, mfe: float, feq: float, ed: float) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    ed_str = f"{ed:.2f}"
    output_path = output_dir / f"{ed_str}_run_{run_index:03d}.txt"
    with output_path.open("w", encoding="utf-8") as out_file:
        out_file.write(f"input_file: {input_file}\n")
        out_file.write(f"run_index: {run_index}\n")
        out_file.write(f"sequence: {seq}\n")
        out_file.write(f"structure: {struc}\n")
        out_file.write(f"mfe: {mfe}\n")
        out_file.write(f"feq: {feq}\n")
        out_file.write(f"ed: {ed}\n")


def _run_revolver_task(task: tuple[str, int, str]) -> None:
    file_path, run_index, output_root = task
    input_path = Path(file_path)
    output_dir = Path(output_root) / input_path.stem

    seq, struc, mfe, feq, ed = revolvr.revolver(str(input_path))
    save_revolver_output(output_dir, run_index, str(input_path), seq, struc, mfe, feq, ed)


def run_revolvers(files: list[str], runs_per_file: int = 1, output_root: str = "revolver_outputs", max_workers: Optional[int] = None) -> None:
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


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python batch_revolvr.py <file1> [<file2> ...] [runs_per_file] [max_workers]")
        sys.exit(1)

    args = sys.argv[1:]
    runs = 1
    max_workers = None
    if args and args[-1].isdigit():
        max_workers = int(args[-1])
        args = args[:-1]
    if args and args[-1].isdigit():
        runs = int(args[-1])
        args = args[:-1]

    run_revolvers(args, runs_per_file=runs, max_workers=max_workers)
