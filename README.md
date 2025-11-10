# vulnscanner - POC Local

This is a Proof-Of-Concept vulnerability scanner orchestrator for lab use.
It runs **nmap**, **nikto** and **whatweb** (external tools must be installed in your environment).

## Structure
- app.py             # Flask API (runs on port 5050)
- scanner/           # runners for each tool
- parsers/           # simple parsers / placeholders
- reports/           # generated per-job outputs (ignored in git)

## Quick start (lab)
1. Make sure `nmap`, `nikto` and `whatweb` are installed and available in PATH.
   Example (Debian/Kali): `sudo apt update && sudo apt install -y nmap nikto`
   (WhatWeb may require `gem` or `apt` package depending on your distro.)
2. Create a Python venv and install requirements:
   ```
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Run the app:
   ```
   python app.py
   ```
   The API will listen on `http://0.0.0.0:5050`.

## Endpoints
- `POST /scan` JSON body: {"target": "example.com"} → starts a synchronous scan (POC).
- `GET /report/<job_id>/meta` → returns the job metadata JSON.

## Notes / Warnings
- **Legal**: only scan targets you have explicit authorization to test.
- This POC runs tools synchronously and **blocks**; for production use a task queue (Celery/RQ) and better isolation (containers).
- Improve input validation before using in any shared network.
