#!/bin/bash
# Compile templates from YAML to JSON

cd "$(dirname "$0")"
python3 compiler.py

