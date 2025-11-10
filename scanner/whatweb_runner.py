import subprocess, shlex
from pathlib import Path
import time

def run_whatweb(target, outdir):
    outdir = Path(outdir); outdir.mkdir(parents=True, exist_ok=True)
    json_path = outdir / "whatweb.json"
    # --log-json writes a JSON lines file
    cmd = f"whatweb --log-json {json_path} {shlex.quote(target)}"
    start = time.time()
    try:
        proc = subprocess.run(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=300)
        rc = proc.returncode
        stdout = proc.stdout
        stderr = proc.stderr
    except Exception as e:
        rc = 255
        stdout = ""
        stderr = str(e)
    elapsed = time.time() - start
    return {"cmd": cmd, "returncode": rc, "stdout": stdout, "stderr": stderr, "json": str(json_path), "elapsed": elapsed}
