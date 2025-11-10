import subprocess, shlex
from pathlib import Path
import time

def run_nikto(target, outdir):
    outdir = Path(outdir); outdir.mkdir(parents=True, exist_ok=True)
    xml_path = outdir / "nikto.xml"
    cmd = f"nikto -h {shlex.quote(target)} -o {xml_path} -Format xml"
    start = time.time()
    try:
        proc = subprocess.run(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=3600)
        rc = proc.returncode
        stdout = proc.stdout
        stderr = proc.stderr
    except Exception as e:
        rc = 255
        stdout = ""
        stderr = str(e)
    elapsed = time.time() - start
    return {"cmd": cmd, "returncode": rc, "stdout": stdout, "stderr": stderr, "xml": str(xml_path), "elapsed": elapsed}
