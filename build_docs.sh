#!/bin/bash

#PROJECT_PATH="."
#cd $PROJECT_PATH || exit
#cd docs || exit
python -m venv .venv_doc

# Check if the virtual environment was created successfully
if [ -f ".venv_doc/bin/activate" ]; then
    source .venv_doc/bin/activate
    pip install --upgrade pip
    pip install .[fastui,bs4,sqlmodel,office,docs,dev]

    # Optionally, install any additional packages required for building the docs
    # pip install sphinx sphinx-rtd-theme

    # Run Sphinx to build the HTML documentation
    sphinx-build -b html docs _build/html

    # Deactivate the virtual environment
    deactivate

    echo "Documentation build complete."
else
    echo "Failed to create virtual environment."
fi