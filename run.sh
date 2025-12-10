#!/bin/bash

cd "$(dirname "$0")"

if [ ! -d "venv" ]; then
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt > /dev/null 2>&1
else
    source venv/bin/activate
fi

python convert.py "$@"

