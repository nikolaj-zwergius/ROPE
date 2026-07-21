from rope.definitions.rope_def import ROOT
from rope.model.records import IndexEntry
from rope.model.Module import Module, segmented_module

def build_IndexEntry(index_line:str) -> IndexEntry:
    line_list = index_line.strip().split("|")
    segments = line_list[3].split(",")
    sequnce = line_list[3].replace(",","")
    if len(segments) == 1:
        type = Module
    else:
        type = segmented_module
    entry = IndexEntry(
        symbol= line_list[0],
        name=line_list[1],
        path=line_list[2],
        len=len(sequnce.replace("^","")),
        priority=int(line_list[4]),
        sequence=sequnce,
        segments=segments,
        type=type
    )
    return entry

def load_index():
    indexentry_lib = {}
    index_lines = read_index()
    for line in index_lines:
        entry = build_IndexEntry(line)
        indexentry_lib[entry.symbol] = entry
    return indexentry_lib

def read_index():
    index_lines = []
    with open(ROOT/"data"/"index","r") as f:
        for line in f:
            index_lines.append(line)
    return index_lines
            


def write_index(index_values:list[str]):
    with open(ROOT/"data"/"index","w") as f:
        for line in index_values:
            f.write(line)