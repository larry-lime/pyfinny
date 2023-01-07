#!/bin/zsh

# Detect if $VIRTUAL_ENV is set and if not, set it to the current directory
if [ -z "$VIRTUAL_ENV" ]; then
  source bin/activate
fi
python3 src/temp.py
