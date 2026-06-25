@echo off
set SCRIPT_DIR=%~dp0
set ROOT_DIR=%SCRIPT_DIR%..
python "%ROOT_DIR%\src\toolstrace.py %*