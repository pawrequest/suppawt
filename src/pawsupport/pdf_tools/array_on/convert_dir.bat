@echo off
set PYTHON_EXE=R:\paul_notes\pss\array_on\.venv_array\Scripts\python.exe
set SCRIPT_PATH=R:\paul_notes\pss\array_on\array_dir\array_directory_pdfs_a4_landscape.py

"%PYTHON_EXE%" "%SCRIPT_PATH%" --input_dir %~dp0

pause
