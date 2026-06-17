@echo off
set local=%~dp0
echo local
echo %~dp0
python %~dp0\trace_analysis.py %*