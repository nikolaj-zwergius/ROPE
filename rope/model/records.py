from dataclasses import dataclass
from rope.model.Module import Module,segmented_module
from enum import Enum




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
    module:str|None
    reports:list[ValidationResult]
    validated:bool
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



@dataclass
class BuildResult:
    build = bool

