#!/usr/bin/bash

export TESTING=true
python3 -m unittest discover -v -s tests -p "test_*.py"
