@echo off
set PYTHON_EXE=R:\paul_r\programs\array_pdfs\.venv\Scripts\python.exe
set SCRIPT_PATH=R:\paul_r\programs\array_pdfs\array.py

"%PYTHON_EXE%" "%SCRIPT_PATH%" %~dp0 --print

pause
