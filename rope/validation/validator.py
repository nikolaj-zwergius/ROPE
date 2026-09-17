from rope.io.package_discover import find_packages
from rope.io.index_handler import load_index, write_index, index_line_maker
from rope.model.records import ValidationStatus,ValidationResult,ValidationReport,Validationcontext
from rope.io.toml_io import load_toml
try:from tomllib import TOMLDecodeError
except ImportError: from tomli import TOMLDecodeError
from pathlib import Path

def validator():
    packages,_,_,_ = find_packages()
    index = load_index()
    master_report:list[ValidationReport] = []
    
    for package in packages:
        context = Validationcontext(package=package,global_skip = False,path=package.parent)
        report = ValidationReport(
            package=package.parent.stem,
            path = package,
            module=None,
            reports=[],
            validated=ValidationStatus.FAIL,
            indexed=False
        )
        result = validate_toml(context)
        report.reports.append(result)
        if result.status == ValidationStatus.FAIL:
            context.global_skip = False
        
        result = validate_files(context)
        report.reports.append(result)
        if result.status == ValidationStatus.FAIL:
            context.global_skip = False

        result = validate_index_state(context,index)
        report.reports.append(result)
        if result.status == ValidationStatus.FAIL:
            global_skip = False

        for i in report.reports:
            #print(package.parent.stem,i.stage,i.status)
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
    validation_reporter(master_report)

def validation_reporter(master_report:list[ValidationReport]):
    for report in master_report:
        print(report.package, report.validated)
        if report.validated == ValidationStatus.PASS:
            continue
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


def validate_toml(context:Validationcontext):
    result = ValidationResult(
        stage="TOML Validation",
        status=ValidationStatus.FAIL,
        warnings=[],
        functional_warnings =[],
        errors=[],
        functional_error = []
    )
    try:
        toml = load_toml(context.package)
    except TOMLDecodeError as e:
        result.errors.append(
            ("TomlLoadError",str(e)))
        return result
    
    _validate_toml_sections(toml, result)
    _validate_toml_fields(toml,result)
    _validate_toml_types(toml,result)


    ### missing variant logic
    if len(result.errors) == 0:
        context.toml = toml
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
    warning_type = "Missing recommend field"
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
    if module.get("priority") is None:
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
    if module.get("nonstandard") is None:
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

def validate_files(context:Validationcontext):
    result = ValidationResult(
        stage="File Validation",
        status=ValidationStatus.FAIL,
        warnings=[],
        functional_warnings =[],
        errors=[],
        functional_error=[]
    )
    if context.global_skip:
        result.status = ValidationStatus.SKIP
        return result
    
    _validate_extra_files_exist(context,result)
    if len(result.errors) > 0:
        return result

    _validate_pdb_files(context,result)


    if len(result.errors) == 0:
        result.status =  ValidationStatus.PASS
    return result

def _validate_pdb_files(context:Validationcontext,result:ValidationResult):
    assert context.toml is not None
    error_type = "PDB Format Error"
    pdb_files = []
    toml = context.toml
    file = toml.get("default",{}).get("file")
    variant = toml.get("variant",{})
    main_failed = False
    test_default = _pdb_logic(context.path/file,error_type)
    if not test_default:
        main_failed = True
        result.errors.extend(test_default)
    pdb_files.append(file)

    for key in variant:
        file = variant[key].get("file")
        result.functional_error.extend(_pdb_logic(context.path/file,error_type))
        pdb_files.append(file)


    context.pdbs = pdb_files


def _pdb_logic(file:Path,error_type:str) -> list[tuple]:
    errors = []


    return errors


def _validate_extra_files_exist(context:Validationcontext,result:ValidationResult):
    assert context.toml is not None
    assert context.path is not None
    error_type = "File not found"
    try:
        open(context.path/context.toml.get("default",{}).get("file"))
    except FileNotFoundError:
        result.errors.append((error_type,"No pdb found for default"))
    if context.toml.get("variant"):

        variants = context.toml.get("variant",{})
        for variant in context.toml.get("variant",{}):
            file = variants[variant].get("file")
            try: open(context.path/file)
            except FileNotFoundError:
                result.errors.append((error_type,f"No pdb found for variant {variant}"))


def validate_index_state(context:Validationcontext,index:dict):
    assert context.toml is not None
    error_type = "Index Error"
    result = ValidationResult(
        stage="Index Validation",
        status=ValidationStatus.FAIL,
        warnings=[],
        functional_warnings =[],
        errors=[],
        functional_error=[]
    )
    toml = context.toml
    if context.global_skip:
        result.status = ValidationStatus.SKIP
        return result
    symbol = toml.get("module",{}).get("symbol")
    name = toml.get("metadata",{}).get("name")
    sequence = toml.get("module",{}).get("sequence")
    path = str(Path(context.path.parent.stem)/Path(context.path.stem))
    if symbol in index:
        if path != index[symbol].path:
            result.errors.append((error_type,f"Symbol {symbol} already assigned to {index[symbol].path}"))
    for i in index.keys():
        if name == index[i].name and symbol != index[i] and path != index[i].path:
            result.errors.append((error_type,f"Name {name} already assigned to {index[symbol].path}"))
    for i in index.keys():
        if sequence == index[i].sequence and symbol != index[i] and path != index[i].path:
            result.errors.append((error_type,f"Sequence in {path} is identical to {index[symbol].path}"))
    if len(result.errors) == 0:
        result.status = ValidationStatus.PASS
    return result


if __name__ == "__main__":
    validator()