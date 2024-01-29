@echo off
set PROJECT_DIR=.
set VENV_NAME=.venv-doc
python -m venv "%PROJECT_DIR%\%VENV_NAME%"
call "%PROJECT_DIR%\%VENV_NAME%\Scripts\activate.bat"
python -m pip install --upgrade pip

cd /d "%PROJECT_DIR%"
pip install .[fastui,bs4,sqlmodel,office,docs,dev]

sphinx-build -b html "%PROJECT_DIR%\docs" "%PROJECT_DIR%\docs\_build"

call deactivate

echo Documentation build complete.
pause
