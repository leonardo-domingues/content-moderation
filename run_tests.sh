#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
export PYTHONPATH=$SCRIPT_DIR

python3 -m pytest $SCRIPT_DIR/tests/test_ContentModerator.py
python3 -m pytest $SCRIPT_DIR/tests/test_DatabaseManager.py
