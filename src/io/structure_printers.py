
from src.core.grid_mapping import  COMPLEMENT_WINDOW, DUPLICATE_WINDOW
from src.definitions.rope_def import VALID_BASES, NUCLEOTIDE_CHARS
from io import TextIOWrapper
from numpy import ndarray
from pathlib import Path
import src.core.revolvr as revolvr
import src.definitions.rope_def as rd
import numpy as np



def render_pattern(out:TextIOWrapper,message:str,data:list,n_map:list,grid:ndarray):
    out.write(message)
    for i in range(grid.shape[0]):
        row_chars = []
        for j in range(grid.shape[1]):
            ch = grid[i][j]
            if ch in NUCLEOTIDE_CHARS:
                row_chars.append(render_cell(ch, data, n_map, i, j))
            else:
                row_chars.append(ch)
        out.write("".join(row_chars) + "\n")

def render_strand_cell(ch:str, i:int, j:int, strand_dir:dict):
    if ch == "p" or ch == "!" or ch == "*":
        direction = strand_dir.get((i, j), "right")
        if direction not in {"rigth", "left"}:
            return "┊"
        return "─"
    if ch in NUCLEOTIDE_CHARS:
        direction = strand_dir.get((i, j), "right")
        if direction in {"up", "down"}:
            return "┊"
        return "─"
    return ch


def render_cell(ch:str, type_list:list, n_map:list, i:int, j:int) -> str:
    if ch in NUCLEOTIDE_CHARS:
        idx = n_map.get((i, j), None)
        if idx is not None and 0 <= idx <= len(type_list):
            return type_list[idx]
    return ch


def structure_printer(output:TextIOWrapper, grid:ndarray, seq_output:str, repeat_map:list, wobbles_seq:list, barriers:list,complement_zones:int, duplicate_zones:int, pattern_repeats:int, poly_repeats:int, restriction_sites:int,n_map:dict,strand_dir:dict,problem:list|None=None):
        
        output.write("2D diagram with sequence\n")
        for i in range(grid.shape[0]):
            row_chars = [grid[i][j] for j in range(grid.shape[1])]
            output.write("".join(row_chars) + "\n")

        output.write("\n\nStrand Path\n")
        for i in range(grid.shape[0]):
            row_chars = [render_strand_cell(grid[i][j], i, j, strand_dir) for j in range(grid.shape[1])]
            output.write("".join(row_chars) + "\n")

        if seq_output.count("N") == 0:
            output.write("\n")
            sequence_array = list(seq_output)
            sequence_check = all(ch in VALID_BASES for ch in sequence_array)
            if not sequence_check:
                message ="\nSequence not suitable for pattern search.  Must only contain A, U C and G. \n"
            else:
                message= f"""\n\nHighlighting Repeat Sequences \n
                WC complement region (P) {COMPLEMENT_WINDOW} or longer: {complement_zones} nts
                Duplicated region (D) {DUPLICATE_WINDOW} or longer: {duplicate_zones} nts
                Strong/Weak region (S/W) 8 or longer: {pattern_repeats} nts
                5 or more in a row of the same nucleotide (A,U,C,G): {poly_repeats} nts
                Common restriction site (X): {restriction_sites} nts
                \n"""
            render_pattern(output,message,repeat_map,n_map,grid)
            render_pattern(output,"\n\nHighlighting GU Pairs\n",wobbles_seq,n_map,grid)
        render_pattern(output,"\n\nHighlighting Structural Barriers\n\n",barriers,n_map,grid)


def analysis_out(outfile,name,structure_map, grid, seq_output, repeat_map, wobbles_seq, barriers, complement_zones, duplicate_zones, pattern_repeats, poly_repeats, restriction_sites, n_map, strand_dir):
    with open(f"{outfile}", "w", encoding="utf-8") as output:
            output.write(f"{name}\n")
            output.write(f"{structure_map}\n")
            output.write(f"{seq_output}\n\n")
            output.write("My Structure map:  \n")
            output.write(f"{structure_map} \n\n")
            structure_printer(output, grid, seq_output, repeat_map, wobbles_seq, barriers, complement_zones, duplicate_zones, pattern_repeats, poly_repeats, restriction_sites, n_map, strand_dir)
            return grid, seq_output, repeat_map, wobbles_seq, barriers, complement_zones, duplicate_zones, pattern_repeats, poly_repeats, restriction_sites, n_map, strand_dir

def save_revolver_output(output_dir: Path, run_index: int, input_file: str, seq: str, struc: str, mfe: float, feq: float, ed: float,problem_mask:list,init_seq:str,analysis_values:tuple[ndarray,str,list[str],list[str],list[str],int,int,int,int,int,dict,dict]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    ed_str = f"{ed:.2f}"
    output_path = output_dir / f"{ed_str}_run_{run_index:03d}.txt"
    grid, seq_output, repeat_map, wobbles_seq, barriers, complement_zones, duplicate_zones, pattern_repeats, poly_repeats, restriction_sites, n_map, strand_dir = analysis_values
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


def flip_pattern(file)->None:
     pattern = rd.generate_np_pattern(file)
     with open("flip.txt","w",encoding="utf-8") as f:
        f.write("Input file:")
        f.write("\n")
        for row in pattern:
            test = "".join(row)
            f.write(test)
            f.write("\n")
        f.write("\n")
        f.write("\n")

        for options in rd.flips:
            f.write(options[2])
            f.write("\n")
            
            for row in np.flip(pattern,options[0]):
                flip_table=options[1]
                for i in range(len(row)):
                    if row[i] in flip_table.keys():
                        row[i] = flip_table[row[i]]
                test = "".join(row)
                f.write(test)
                f.write("\n")
            f.write("\n")
            f.write("\n")

def trace_pattern_out(file:str,seq:str,base_pair:str) -> None:
    with open(file, "r") as f:
        name = f.readline().rstrip().lstrip(">")

    with open("target.txt","w") as output:
       output.write(name)
       output.write("\n")
       output.write(base_pair)
       output.write("\n")
       output.write(seq)