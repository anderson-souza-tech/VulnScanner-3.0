
from flask import Blueprint, render_template, request, redirect, url_for, session
from scanner.nmap_scan import scan_tcp_udp
from scanner.nikto_scan import run_nikto
from scanner.whatweb_scan import run_whatweb
from scanner.dirb_scan import run_dirb
from datetime import datetime
import os
import pathlib

main = Blueprint("main", __name__)

base_path = pathlib.Path(__file__).resolve().parent.parent

@main.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        senha = request.form.get("senha")
        if senha == "Vulnér@2024!":
            session["logado"] = True
            return redirect(url_for("main.dashboard"))
        else:
            return render_template("login.html", erro="Senha incorreta")
    return render_template("login.html")

@main.route("/dashboard")
def dashboard():
    if not session.get("logado"):
        return redirect(url_for("main.login"))
    return render_template("dashboard.html")

@main.route("/scan", methods=["GET", "POST"])
def scan():
    if not session.get("logado"):
        return redirect(url_for("main.login"))

    resultado = {}
    arquivo = None
    if request.method == "POST":
        target = request.form.get("target")

        resultado["nmap"] = scan_tcp_udp(target)
        resultado["nikto"] = run_nikto(target)
        resultado["whatweb"] = run_whatweb(target)
        resultado["dirb"] = run_dirb(target)

        results_dir = os.path.join(base_path, "static", "results")
        os.makedirs(results_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"scan_{target.replace('.', '_').replace(':', '_')}_{timestamp}.txt"
        filepath = os.path.join(results_dir, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            for tool, output in resultado.items():
                f.write(f"===== {tool.upper()} =====\n{output}\n\n")

        arquivo = os.path.join("results", filename)

    return render_template("scan.html", resultado=resultado, arquivo=arquivo)

@main.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("main.login"))
