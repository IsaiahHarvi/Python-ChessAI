#!/bin/bash

# Get the absolute path of the parent directory of the script
parent_dir=$(dirname "$(realpath "$0")")/..

# Set PYTHONPATH to the parent directory
export PYTHONPATH="$parent_dir/src"

# Run pytest
pytest -s