from flask import Flask, request, jsonify, send_file
from uuid import uuid4
from pathlib import Path
import json

# Runners
from scanner.nmap_runner import run_nmap
from scanner.nikto_runner import run_nikto
from scanner.whatweb_runner import run_whatweb

app = Flask(__name__)

# Pasta de relatórios
REPORTS = Path("reports")
REPORTS.mkdir(exist_ok=True)

# Health-check / teste via browser
@app.route("/", methods=["GET"])
def index():
    return "vulnscanner POC – server running", 200

# Dispara um scan síncrono (POC)
@app.route("/scan", methods=["POST"])
def scan():
    data = request.get_json(silent=True) or {}
    target = data.get("target")
    if not target:
        return jsonify({"error": "target required"}), 400

    job_id = str(uuid4())
    job_dir = REPORTS / job_id
    job_dir.mkdir(parents=True, exist_ok=True)

    # Execução (POC). Em produção, ideal usar fila/worker.
    nmap_res = run_nmap(target, job_dir)
    nikto_res = run_nikto(target, job_dir)
    whatweb_res = run_whatweb(target, job_dir)

    meta = {
        "target": target,
        "job_id": job_id,
        "nmap": nmap_res,
        "nikto": nikto_res,
        "whatweb": whatweb_res,
    }
    meta_path = job_dir / "meta.json"
    with meta_path.open("w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)

    # 202 Accepted porque o trabalho foi criado/executado
    return jsonify({"job_id": job_id, "meta": meta}), 202

# Baixa o meta do job
@app.route("/report/<job_id>/meta", methods=["GET"])
def get_meta(job_id: str):
    meta_path = REPORTS / job_id / "meta.json"
    if not meta_path.exists():
        return jsonify({"error": "not found"}), 404
    return send_file(str(meta_path), mimetype="application/json")


if __name__ == "__main__":
    # Permite rodar com: python app.py
    app.run(host="0.0.0.0", port=5050, debug=True)
