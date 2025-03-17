#!/usr/bin/env python3
#Create a flask app that exposes an API
import ipaddress
import argparse
import json
from flask import Flask, request, render_template, jsonify
import os
import subprocess

app = Flask(__name__)

def subnet_ipv6(prefix: str, new_prefix: int):
    try:
        network = ipaddress.IPv6Network(prefix, strict=False)
        if new_prefix <= network.prefixlen:
            return {"error": "New prefix must be larger than the original prefix."}, []
        
        subnets = list(network.subnets(new_prefix=new_prefix))
        
        warning = None
        if new_prefix % 4 != 0:
            warning = "Warning: This will not output prefixes on a nibble boundary."
        
        return {"warning": warning}, subnets
    except ValueError as e:
        return {"error": f"Invalid input: {e}"}, []

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        prefix = request.form.get("subnet")
        new_prefix = request.form.get("prefix")
        
        if not prefix or not new_prefix.isdigit():
            return render_template("index.html", error="Invalid input.")
        
        new_prefix = int(new_prefix)
        message, subnets = subnet_ipv6(prefix, new_prefix)
        
        if "error" in message:
            return render_template("index.html", error=message["error"])
        
        return render_template("index.html", subnets=subnets, warning=message.get("warning"))
    
    return render_template("index.html")

@app.route("/api/subnet", methods=["GET"])
def api_subnet():
    prefix = request.args.get("subnet")
    new_prefix = request.args.get("prefix")
    
    if not prefix or not new_prefix or not new_prefix.isdigit():
        return jsonify({"error": "Invalid input."}), 400
    
    new_prefix = int(new_prefix)
    message, subnets = subnet_ipv6(prefix, new_prefix)
    
    if "error" in message:
        return jsonify({"error": message["error"]}), 400
    
    return jsonify({"warning": message.get("warning"), "subnets": [str(subnet) for subnet in subnets]})

def run_app(daemon=False):
    if daemon:
        print("Running in daemon mode...")
        subprocess.Popen(["gunicorn", "--daemon", "--bind", "[]::1]:5000", "app:app"])
    else:
        app.run(debug=True, host="[::1]")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="IPv6 Subnet Planner Web App")
    parser.add_argument("-d", "--daemon", action="store_true", help="Run the app as a daemon")
    
    args = parser.parse_args()
    run_app(daemon=args.daemon)
