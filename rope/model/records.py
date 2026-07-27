from dataclasses import dataclass
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
    stage: str
    status: ValidationStatus
    warnings: list[tuple]
    functional_warnings: list[tuple]
    errors: list[tuple]

@dataclass
class ValidationReport:
    pakage:str
    path:Path
    module:str|None
    reports:list[ValidationResult]
    validated:ValidationStatus
    indexed: bool

@dataclass
class IndexEntry:
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
    build:list
    last_build:ndarray
    seq:str
    output:TextIOWrapper
    atom_count:int = 1
    residue_count:int = 1
    seq_index:int = 0
    
    

@dataclass
class BuildResult:
    build = bool

