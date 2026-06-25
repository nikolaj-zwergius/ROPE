@echo off
set SCRIPT_DIR=%~dp0
set ROOT_DIR=%SCRIPT_DIR%..
python "%ROOT_DIR%\src\io\pdb_file_cleaner.py


if "%~1"=="fold" goto fold_jmp
if "%~1"=="analyse" goto analysis_jmp
if "%~1"=="build" goto build_jmp
if "%~1"=="dragon" goto dragon_jmp

goto error

:fold_jmp
set "jmp_loc_v=fold"
goto remainder

:analysis_jmp
set "jmp_loc_v=analysis"
goto remainder

:build_jmp
set "jmp_loc_v=build"
goto remainder

:dragon_jmp
set "jmp_loc_v=dragon"
goto remainder

:remainder
setlocal enabledelayedexpansion

set "first=%~1"
shift

set "rest="

:loop
if "%~1"=="" goto done
set "rest=!rest! "%~1""
shift
goto loop

:done
goto jmp_loc

:jmp_loc

if "%jmp_loc_v%"=="fold" goto fold_func
if "%jmp_loc_v%"=="analysis" goto analysis_func
if "%jmp_loc_v%"=="build" goto build_func
if "%jmp_loc_v%"=="dragon" goto dragon_func

goto error_jmp


:build_func
python "%ROOT_DIR%\src\tools\build.py" %rest%
goto end
:fold_func
python "%ROOT_DIR%\src\tools\batch_revolvr.py" %rest%
goto end
:analysis_func
python "%ROOT_DIR%\src\tools\analysis.py" %rest%
goto end
:dragon_func
python "%ROOT_DIR%\src\tools\continuous_revolvr.py" %rest%
goto end
:error
python "%ROOT_DIR%\src\utils\cli_errors.py" %*
goto end

:error_jmp
echo jump not working as intended
goto end


:end
