#! /bin/bash

echo "Building wheel..."
python setup.py bdist_wheel

echo "Installing in empi venv..."
source "/Users/prof.mannyman/Documents/coding/empi/.venv/bin/activate"
pip install -e .