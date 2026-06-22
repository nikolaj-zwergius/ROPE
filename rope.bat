@echo off

set "local=%~dp0"
python %local%\RNA_lib\pdb_file_cleaner.py %rest%


if "%~1"=="fold" goto fold_jmp
if "%~1"=="analyse" goto analysis_jmp
if "%~1"=="build" goto build_jmp

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

goto error_jmp


:build_func
python %local%\RNAbuild.py %rest%
goto end
:fold_func
python %local%\batch_revolvr.py %rest%
goto end
:analysis_func
python %local%\trace_analysis.py %rest%
goto end

:error
python %local%\rope_helper.py %*
goto end

:error_jmp
echo jump not working as intended
goto end


:end
