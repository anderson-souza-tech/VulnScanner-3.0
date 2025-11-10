#!/bin/bash
# simple helper to run the app in dev
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
echo "Run: python app.py"
