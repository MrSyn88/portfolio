#!/usr/bin/bash

export TESTING=true
"$PWD"/python3-virtualenv/bin/python -m unittest discover -vbk "test_*" tests/