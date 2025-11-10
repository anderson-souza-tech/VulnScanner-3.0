import json
from pathlib import Path

def parse_whatweb_json(json_path):
    p = Path(json_path)
    if not p.exists():
        return {"error":"file not found", "path": str(p)}
    items = []
    with open(p, 'r', encoding='utf-8') as f:
        for ln in f:
            ln = ln.strip()
            if not ln:
                continue
            try:
                items.append(json.loads(ln))
            except Exception:
                # not strictly JSON-lines? attempt fallback
                try:
                    items.append(json.loads(ln.replace("'","\"")))
                except Exception as e:
                    items.append({"parse_error": str(e), "raw": ln})
    return items
