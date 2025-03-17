#!/usr/bin/env python3
#Create a flask app that exposes an API
import ipaddress
import argparse
import json
import os
import sys
from flask import Flask, request, jsonify, render_template

# Ensure Flask finds templates even when daemonized
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

app = Flask(__name__, template_folder=TEMPLATES_DIR)

def subnet_ipv6(prefix: str, new_prefix: int):
    """Generate subnets from an IPv6 prefix."""
    try:
        network = ipaddress.IPv6Network(prefix, strict=False)
        if new_prefix <= network.prefixlen:
            return {"error": "New prefix must be larger than the original prefix."}, []
        
        subnets = list(network.subnets(new_prefix=new_prefix))
        
        warning = None
        if new_prefix % 4 != 0:
            warning = "Warning: This will not output prefixes on a nibble boundary. Maybe rethink what you are doing?"
        
        return {"warning": warning}, subnets
    except ValueError as e:
        return {"error": f"Invalid input: {e}"}, []

@app.route("/")
def home():
    """Render the main web UI."""
    return render_template("index.html")  # Make sure 'templates/index.html' is in the right place.

@app.route("/api/subnet", methods=["POST"])
def api_subnet():
    """API endpoint to generate subnets via POST requests from the web form."""
    
    prefix = request.form.get("subnet")  # Extract from form data
    new_prefix = request.form.get("prefix")

    if not prefix or not new_prefix or not new_prefix.isdigit():
        return jsonify({"error": "Invalid input. Please enter a valid IPv6 prefix and prefix size."}), 400

    new_prefix = int(new_prefix)
    message, subnets = subnet_ipv6(prefix, new_prefix)

    if "error" in message:
        return jsonify({"error": message["error"]}), 400

    return jsonify({"warning": message.get("warning"), "subnets": [str(subnet) for subnet in subnets]})

def daemonize():
    """Daemonize the process to run in the background."""
    pid = os.fork()
    if pid > 0:
        print(f"Daemon started with PID {pid}")
        sys.exit(0)  # Parent exits, leaving child process running

    os.setsid()  # Create a new session

    pid = os.fork()
    if pid > 0:
        sys.exit(0)  # Exit second parent

    sys.stdout.flush()
    sys.stderr.flush()

    with open('/dev/null', 'r') as devnull, open('/tmp/ipv6_subnet_planner.log', 'a+') as logfile:
        os.dup2(devnull.fileno(), sys.stdin.fileno())
        os.dup2(logfile.fileno(), sys.stdout.fileno())
        os.dup2(logfile.fileno(), sys.stderr.fileno())

    os.chdir(BASE_DIR)  # Ensure Flask uses the correct working directory
    app.run(host="::1", port=5000)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="IPv6 Subnet Planner Web App")
    parser.add_argument("-d", "--daemon", action="store_true", help="Run the app as a daemon")

    args = parser.parse_args()

    if args.daemon:
        daemonize()
    else:
        os.chdir(BASE_DIR)  # Ensure correct path for templates
        app.run(debug=True, host="::1")
