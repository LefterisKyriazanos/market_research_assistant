#!/bin/bash

# Create virtual environment
python3.9 -m venv .venv

# Install requirements
source .venv/bin/activate
pip install -r requirements.txt

# Activate virtual environment
source .venv/bin/activate

# --------------------------------------------------------------
# Execute from cli
# --------------------------------------------------------------
# chmod +x setup.sh
# ./setup.sh
