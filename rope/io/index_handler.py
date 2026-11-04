from typing import Any, Mapping

from rope.definitions.rope_def import ROOT
from rope.model.records import IndexEntry
from rope.model.Module import Module, segmented_module
from pathlib import Path


def build_IndexEntry(index_line: str) -> IndexEntry:
    """Parse one pipe-delimited module index row into an :class:`IndexEntry`.

    The row's sequence column also encodes alternating segments and spacers;
    ``^`` markers are excluded from the reported length. Malformed rows or
    non-integer priorities raise the corresponding parsing exception.
    """
    line_list = index_line.strip().split("|")
    segments = line_list[3].split(",")[0::2]
    sequence = line_list[3].replace(",","")
    constrains=line_list[5].split(",")
    has_constrains = False
    if constrains != [""]:
        has_constrains = True
    if len(segments) == 1:
        type = Module
    else:
        type = segmented_module
    entry = IndexEntry(
        symbol= line_list[0],
        name=line_list[1],
        path=line_list[2],
        len=len(sequence.replace("^","")),
        priority=int(line_list[4]),
        sequence=sequence,
        segments=segments,
        type=type,
        has_constrain= has_constrains,
        constrains=constrains,
        index_line = index_line.strip()
    )
    return entry


def load_index() -> dict[str, IndexEntry]:
    indexentry_lib = {}
    index_lines = read_index()
    for line in index_lines:
        entry = build_IndexEntry(line)
        indexentry_lib[entry.symbol] = entry
    return indexentry_lib


def read_index() -> list[str]:
    index_lines = []
    with open(ROOT/"data"/"index","r",encoding="utf-8") as f:
        for line in f:
            index_lines.append(line)
    return index_lines
            


def index_line_maker(toml: Mapping[str, Any], path: Path) -> tuple[str, str]:
    """Build the index row and optional variant-index row for a module TOML.

    The first result is the module row. The second is empty when there are no
    variants; otherwise it has the form ``symbol|default|variant,variant``.
    """
    index_line = []
    
    
    index_line.append(toml.get("module",{}).get("symbol"))
    index_line.append(toml.get("metadata",{}).get("name"))
    index_line.append(str(Path(path.parent.parent.stem)/path.parent.stem))
    if toml.get("module",{}).get("type") == "segmented":
        
        segments = toml.get("module",{}).get("segments")
        spacer = toml.get("module",{}).get("spacer")
        string = segments[0] +","
        for i in range(len(spacer)):
            string += spacer[i] +","
            string += segments[i+1]
        index_line.append(string)
    else:
        index_line.append(toml.get("module",{}).get("sequence",""))
    index_line.append(str(toml.get("module",{}).get("priority",0)))
    index_line.append(",".join(toml.get("module",{}).get("constraints","")))

    variants = toml.get("variant",{}).keys()
    variant_list= []
    variant_line =""
    if variants:
        default_name = toml.get("default",{}).get("name","default")
        for variant in variants:
           variant_list.append(variant)
        variant_line = toml.get("module",{}).get("symbol")+"|"+default_name+"|"+",".join(variant_list)
    return "|".join(index_line), variant_line


def write_index(index_values: list[str], variant_index: list[str]) -> None:
    with open(ROOT/"data"/"index","w") as f:
        for line in index_values:
            f.write(line+"\n")
    with open(ROOT/"data"/"variant_index","w",encoding="utf-8") as f:
        for line in variant_index:
            if line:
                f.write(line+"\n")


def load_variant_index() -> dict[str, list[str]]:
    lines = {}
    with open(ROOT/"data"/"variant_index","r") as f:
        for line in f:
            line = line.split("|")
            default = [line[1] + " (default)"]
            
            lines[line[0]] = default + line[2].split(",")

    return lines