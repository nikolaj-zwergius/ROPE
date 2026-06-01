
from utils.trace_utils import  COMPLEMENT_WINDOW, DUPLICATE_WINDOW
from utils.rope_def import VALID_BASES, NUCLEOTIDE_CHARS


def render_pattern(out,message,data,n_map,grid):
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

def render_strand_cell(ch, i, j, strand_dir):
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


def render_cell(ch, type_list, n_map, i, j):
    if ch in NUCLEOTIDE_CHARS:
        idx = n_map.get((i, j), None)
        if idx is not None and 1 <= idx <= len(type_list):
            return type_list[idx - 1]
    return ch


def structure_printer(output, grid, seq_output:str, repeat_map:list, wobbles_seq:list, barriers:list,complement_zones:int, duplicate_zones:int, pattern_repeats:int, poly_repeats:int, restriction_sites:int,n_map:dict,strand_dir:dict):
        output.write("2D diagram with sequence\n")
        for i in range(grid.shape[0]):
            row_chars = [grid[i][j] for j in range(grid.shape[1])]
            output.write("".join(row_chars) + "\n")

        output.write("\n\nStrand Path\n")
        for i in range(grid.shape[0]):
            row_chars = [render_strand_cell(grid[i][j], i, j, strand_dir) for j in range(grid.shape[1])]
            output.write("".join(row_chars) + "\n")

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

