from dataclasses import dataclass
from typing import Any
from rope.model.Module import Module,segmented_module
from enum import Enum
from pathlib import Path
from numpy import ndarray
from io import TextIOWrapper


class ValidationStatus(Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    SKIP = "SKIP"

@dataclass
class ValidationResult:
    """One validation stage's status and categorized diagnostics.

    Each diagnostic list contains ``(category, message)`` string pairs.
    """

    stage: str
    status: ValidationStatus
    warnings: list[tuple[str, str]]
    functional_warnings: list[tuple[str, str]]
    errors: list[tuple[str, str]]
    functional_error: list[tuple[str, str]]

@dataclass
class ValidationReport:
    """Package-level outcome with its individual validation-stage results.

    ``validated`` summarizes the package; ``indexed`` is the index-state flag
    available to validation helpers.
    """

    package:str
    path:Path
    module:str|None
    reports:list[ValidationResult]
    validated:ValidationStatus
    indexed: bool

@dataclass
class IndexEntry:
    """Module metadata parsed from one pipe-delimited index row.

    ``sequence`` contains the row's segment/spacer text with commas removed;
    ``segments`` contains its segment entries, and ``len`` excludes ``^``
    structural markers. ``type`` selects the module class used by the loader.
    """

    symbol: str
    name: str
    path: str
    len: int
    priority:int
    sequence:str
    segments: list[str]
    type: type[Module]|type[segmented_module]
    has_constrain:bool
    constrains: list[str]
    index_line:str


@dataclass
class BuildState:
    """Mutable build coordinates, sequence position, and PDB output counters.

    The build writer updates this shared state as residues are emitted; atom
    and residue numbering default to 1, and ``seq_index`` defaults to 0.
    """

    build:list[ndarray]
    last_build:ndarray
    seq:str
    output:TextIOWrapper
    atom_count:int = 1
    residue_count:int = 1
    seq_index:int = 0
    
    

@dataclass
class BuildResult:
    """Compatibility record whose ``build`` field defaults to the ``bool`` type.

    It does not represent a build outcome or hold a boolean result value.
    """

    build: type[bool] = bool

@dataclass
class Validationcontext:
    """Mutable inputs and parsed data shared by package-validation helpers.

    ``package`` points to the package TOML file and ``path`` to its directory.
    Helpers may populate the parsed TOML and discovered PDB paths, and use
    ``global_skip`` to communicate whether later checks should be skipped.
    """

    package:Path
    global_skip:bool
    path: Path
    toml: dict[str, Any] | None = None
    pdbs: list[str | None] | None = None
