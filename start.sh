#!/bin/bash

if [ -z "$VIRTUAL_ENV" ]; then
  source bin/activate
fi
python3 src/main.py
