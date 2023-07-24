#!/usr/bin/bash

export TESTING=true
python3 -m unittest discover -vbk "test_*" tests/