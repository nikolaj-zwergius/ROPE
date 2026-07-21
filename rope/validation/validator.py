from rope.io.pakage_disover import find_pakages
from rope.io.index_handler import load_index, write_index, index_line_maker
from rope.model.records import ValidationStatus,ValidationResult,ValidationReport
from rope.io.toml_io import load_toml
from tomllib import TOMLDecodeError
from pathlib import Path
def validator():
    pakages,_,_,_ = find_pakages()
    index = load_index()
    master_report:list[ValidationReport] = []
    global_skip = False
    for pakage in pakages:
        report = ValidationReport(
            pakage=pakage.parent.stem,
            path = pakage,
            module=None,
            reports=[],
            validated=ValidationStatus.FAIL,
            indexed=False
        )
        result = validate_toml(pakage)
        report.reports.append(result)
        if result.status == ValidationStatus.FAIL:
            global_skip = False
        
        result = validate_files(pakage,global_skip)
        report.reports.append(result)
        if result.status == ValidationStatus.FAIL:
            global_skip = False

        result = validate_index_state(pakage,global_skip,index)
        report.reports.append(result)
        if result.status == ValidationStatus.FAIL:
            global_skip = False

        for i in report.reports:
            #print(pakage.parent.stem,i.stage,i.status)
            if i.status == ValidationStatus.FAIL:
                master_report.append(report)
                break
        else:
            report.validated = ValidationStatus.PASS
            master_report.append(report)
    index_lines = []
    variant_lines = []
    used_symbols = []
    for report in master_report:
        if report.validated == ValidationStatus.PASS:
            toml = load_toml(report.path)
            used_symbols.append(toml.get("module",{}).get("symbol"))
            index_line, variant_line = index_line_maker(toml,report.path)
            index_lines.append(index_line)
            variant_lines.append(variant_line)
    for key in index:
        if key not in used_symbols:
            index_lines.append(index[key].index_line)
    write_index(index_lines,variant_lines)

    validattion_reporter(master_report)

def validattion_reporter(master_report:list[ValidationReport]):
    for report in master_report:
        print(report.pakage, report.validated)
        for sub in report.reports:
            print("\t",sub.stage,sub.status)
            if sub.errors:
                print("\t ERRORS:")
                for error in sub.errors:
                    print("\t\t",error)
            if sub.functional_warnings:
                print("\t F warn:")
                for error in sub.functional_warnings:
                    print("\t\t",error)
            if sub.warnings:
                print("\t WARN:")
                for error in sub.warnings:
                    print("\t\t",error)


def validate_toml(path):
    result = ValidationResult(
        stage="TOML Validation",
        status=ValidationStatus.FAIL,
        warnings=[],
        functional_warnings =[],
        errors=[]
    )
    try:
        toml = load_toml(path)
    except TOMLDecodeError as e:
        result.errors.append(
            ("TomlLoadError",str(e)))
        return result
    
    _validate_toml_sections(toml, result)
    _validate_toml_fields(toml,result)
    _validate_toml_types(toml,result)


    ### missing variant logic
    if len(result.errors) == 0:
        result.status = ValidationStatus.PASS
    return result

def _validate_toml_sections(toml,result:ValidationResult):
    error_type = "Missing Section"
    if "metadata" not in toml:
        result.errors.append((error_type, "No metadata section defined"))
    if "module" not in toml:
        result.errors.append((error_type, "No module section defined"))
    if "default" not in toml:
        result.errors.append((error_type, "No default section defined"))

def _validate_toml_fields(toml,result:ValidationResult):
    error_type = "Missing required field"
    fwarning_type = "Missing functional field"
    warning_type = "Missing recommed field"
    metadata = toml.get("metadata",{})
    module = toml.get("module",{})
    default = toml.get("default",{})
    if not metadata.get("name"):
        result.errors.append((error_type, "No metadata.name field defined"))
    if not metadata.get("source"):
        result.warnings.append((warning_type,"No metadata.source field defined"))
    if not module.get("symbol"):
        result.errors.append((error_type, "No module.symbol field defined"))
    if not module.get("type"):
        result.errors.append((error_type, "No module.type field defined"))
    if not module.get("priority"):
        result.functional_warnings.append((fwarning_type,"No module.priority defined"))
    if not default.get("file"):
        result.errors.append((error_type,"No default.file defined"))
    if module.get("nonstandard") is True:
        if not module.get("reason"):
            result.errors.append((error_type,"when nonstandard is true reason must be given"))
    if module.get("nonstandard") is False:
       if module.get("reason"):
           result.errors.append((error_type,"when nonstandard is false no reason must be given"))
    if not module.get("nonstandard") and not module.get("sequence"):
        result.errors.append((error_type,"No module.sequence field defined"))
    if module.get("has_constraints") and not module.get("constraints"):
        result.errors.append((error_type,"No module.constraints field defined"))
    if not module.get("nonstandard"):
        result.functional_warnings.append((fwarning_type,"No module.nonstandard defined"))
    if module.get("has_constraints") is True:
        if not module.get("constraints"):
            result.errors.append((error_type,"when has_constraints is true constraints must be given"))
    if module.get("has_constraints") is False:
       if module.get("constraints"):
           result.errors.append((error_type,"when has_constraints is false no constraints must be given"))

def _validate_toml_types(toml,result:ValidationResult):
    error_type = "Wrong field type"
    metadata = toml.get("metadata",{})
    module = toml.get("module",{})
    default = toml.get("default",{})

    if metadata.get("name") and not type(metadata.get("name")) is str:
        result.errors.append((error_type,"metadata.name not string"))
    if module.get("symbol") and not type(module.get("symbol")) is str:
        result.errors.append((error_type,"module.symbol not string"))
    if "priority" in module and not type(module.get("priority")) is int:
        result.errors.append((error_type,"module.priority not integer"))
    if "nonstandard" in module and not type(module.get("nonstandard")) is bool:
        result.errors.append((error_type,"module.nonstandard not bool"))
    if module.get("reason") and not type(module.get("reason")) is str:
        result.errors.append((error_type,"module.reason not string"))
    if default.get("file") and not type(default.get("file")) is str:
        result.errors.append((error_type,"module.reason not string"))
    if "has_constraints" in module and not type(module.get("has_constraints")) is bool:
        result.errors.append((error_type,"module.has_constraints not bool"))
    if "constraints" in module and not type(module.get("constraints")) is list:
        result.errors.append((error_type,"module.constraints not list"))

def validate_files(path:Path,skipped):
    error_type = "File not found"
    result = ValidationResult(
        stage="File Validation",
        status=ValidationStatus.FAIL,
        warnings=[],
        functional_warnings =[],
        errors=[]
    )
    toml = load_toml(path)
    if skipped:
        result.status = ValidationStatus.SKIP
        return result
    
    try:
        open(path.parent/toml.get("default",{}).get("file"))
    except FileNotFoundError:
        result.errors.append((error_type,"No pdb found for default"))

    if len(result.errors) == 0:
        result.status =  ValidationStatus.PASS
    return result

def validate_index_state(pakage:Path,skipped:bool,index:dict):
    error_type = "Index Error"
    result = ValidationResult(
        stage="Index Validation",
        status=ValidationStatus.FAIL,
        warnings=[],
        functional_warnings =[],
        errors=[]
    )
    toml = load_toml(pakage)
    if skipped:
        result.status = ValidationStatus.SKIP
        return result
    symbol = toml.get("module",{}).get("symbol")
    name = toml.get("metadata",{}).get("name")
    sequence = toml.get("module",{}).get("sequence")
    path = str(Path(pakage.parent.parent.stem)/Path(pakage.parent.stem))
    if symbol in index:
        if path != index[symbol].path:
            result.errors.append((error_type,f"Symbol {symbol} already asigned to {index[symbol].path}"))
    for i in index.keys():
        if name == index[i].name and symbol != index[i] and path != index[i].path:
            result.errors.append((error_type,f"Name {name} already asigned to {index[symbol].path}"))
    for i in index.keys():
        if sequence == index[i].sequence and symbol != index[i] and path != index[i].path:
            result.errors.append((error_type,f"equence in {path} is identical to {index[symbol].path}"))
    if len(result.errors) == 0:
        result.status = ValidationStatus.PASS
    return result


validator()