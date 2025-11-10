import xmltodict
from pathlib import Path

def parse_nikto_xml(xml_path):
    p = Path(xml_path)
    if not p.exists():
        return {"error":"file not found", "path": str(p)}
    with open(p, 'r', encoding='utf-8') as f:
        doc = xmltodict.parse(f.read())
    return doc
