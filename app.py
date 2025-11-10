from flask import Flask, request, jsonify, send_file
from uuid import uuid4
from pathlib import Path
from scanner.nmap_runner import run_nmap
from scanner.nikto_runner import run_nikto
from scanner.whatweb_runner import run_whatweb
import json

app = Flask(__name__)
REPORTS = Path("reports")
REPORTS.mkdir(exist_ok=True)

# Health / index route para testes de browser / health-check
@app.route("/", methods=["GET"])
def index():
    return "vulnscanner POC — server running", 200

@app.route("/scan", methods=["POST"])
def scan():
    data = request.json or {}
    target = data.get("target")
    if not target:
        return jsonify({"error":"target required"}), 400

    job_id = str(uuid4())
    job_dir = REPORTS / job_id
    job_dir.mkdir(parents=True, exist_ok=True)

    # synchronous execution (POC). Em produção, use uma fila/worker.
    nmap_res = run_nmap(target, job_dir)
    nikto_res = run_nikto(target, job_dir)
    whatweb_res = run_whatweb(target, job_dir)

    meta = {"target":target, "nmap":nmap_res, "nikto":nikto_res, "whatweb":whatweb_res}
    with open(job_dir / "meta.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)

    return jsonify({"job_id": job_id, "meta": meta}), 202

@app.route("/report/<job_id>/meta", methods=["GET"])
def get_meta(job_id):
    path = REPORTS / job_id / "meta.json"
    if not path.exists():
        return jsonify({"error":"not found"}), 404
    return send_file(str(path), mimetype="application/json")

if __name__ == "__main__":
    # host 0.0.0.0 para aceitar conexões externas (LAN). Porta 5050 por convenção do POC.
    app.run(host="0.0.0.0", port=5050)
