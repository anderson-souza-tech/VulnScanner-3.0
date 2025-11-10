import subprocess
import shlex
from pathlib import Path
import time

def run_nmap(target, outdir, extra_args="-sV -p- -T4"):
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    xml_path = outdir / "nmap.xml"
    cmd = f"nmap {extra_args} -oX {xml_path} {shlex.quote(target)}"
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
