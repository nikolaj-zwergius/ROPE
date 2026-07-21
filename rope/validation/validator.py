from rope.io.pakage_disover import find_pakages
from rope.io.index_handler import load_index
from rope.model.records import ValidationStatus,ValidationResult,ValidationReport
from rope.io.toml_io import load_toml
from tomllib import TOMLDecodeError

def validator():
    pakages,_,_,_ = find_pakages()
    index = load_index()
    master_report = []
    skip = False
    global_skip = False
    for pakage in pakages:
        report = ValidationReport(
            pakage=pakage.parent.stem,
            module=None,
            reports=[],
            validated=False,
            indexed=False
        )
        result = validate_toml(pakage)
        report.reports.append(result)
        if result.status == ValidationStatus.FAIL:
            global_skip = False

        if result.status == ValidationStatus.FAIL:
            print(report.pakage)
            print("ERROR:")
            for i in result.errors:
                print(i)
            print("Fwarn:")
            for i in result.functional_warnings:
                print(i)
            print("warn")
            for i in result.warnings:
                print(i)


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
    if not module.get("nonstandard") and not module.get("sequence"):
        result.errors.append((error_type,"No module.sequence field defined"))
    if not module.get("nonstandard"):
        result.functional_warnings.append((fwarning_type,"No module.nonstandard defined"))

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
        result.errors.append((error_type,"module.nonstandard not integer"))
    if module.get("reason") and not type(module.get("reason")) is str:
        result.errors.append((error_type,"module.reason not string"))
    if default.get("file") and not type(default.get("file")) is str:
        result.errors.append((error_type,"module.reason not string"))

def validate_toml_schema():
    pass

validator()