#!/usr/bin/env python3
# Create a subnet list for IPv6 address planning. 
# This does not support IPv4 because it is a dead language.
# Hastily cobbled together by buraglio@forwardingplane.net
# Licensed as open with attribution
# Currently there are issues with generating from longer prefixes that I have not figured out, sorry
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

def subnet_ipv6(prefix: str, new_prefix: int, limit=None):
    """Generate subnets from an IPv6 prefix with an optional limit."""
    try:
        network = ipaddress.IPv6Network(prefix, strict=False)
        if new_prefix <= network.prefixlen:
            return {"error": "New prefix must be larger than the original prefix.", "total_subnets": 0}, []
        
        subnets = list(network.subnets(new_prefix=new_prefix))
        
        warning = None
        if new_prefix % 4 != 0:
            warning = "Warning: This will not output prefixes on a nibble boundary. Maybe rethhink what you're doing?"

        total_subnets = len(subnets)

        if limit:
            subnets = subnets[:limit]  # Limit number of displayed subnets

        return {"warning": warning, "total_subnets": total_subnets}, subnets

    except ValueError as e:
        return {"error": f"Invalid input: {e}", "total_subnets": 0}, []

@app.route("/api/subnet", methods=["POST"])
def api_subnet():
    """API endpoint to generate subnets via POST requests from the web form."""
    
    prefix = request.form.get("subnet")
    new_prefix = request.form.get("prefix")
    limit = request.form.get("limit")

    if not prefix or not new_prefix or not new_prefix.isdigit():
        return jsonify({"error": "Invalid input. Please enter a valid IPv6 prefix and prefix size."}), 400

    new_prefix = int(new_prefix)
    limit = int(limit) if limit and limit.isdigit() else None

    message, subnets = subnet_ipv6(prefix, new_prefix, limit)

    if "error" in message:
        return jsonify({"error": message["error"]}), 400

    return jsonify({
        "warning": message.get("warning"),  # Include warning if applicable
        "total_subnets": message["total_subnets"],
        "subnets_shown": len(subnets),
        "subnets": [str(subnet) for subnet in subnets]
    })

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
    app.run(host="0.0.0.0", port=5000)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="IPv6 Subnet Planner Web App")
    parser.add_argument("-s", "--subnet", help="IPv6 prefix (e.g., 2001:db8::/32)")
    parser.add_argument("-p", "--prefix", type=int, help="New subnet prefix length (e.g., 48)")
    parser.add_argument("-o", "--output", help="Output file name")
    parser.add_argument("-j", "--json", action="store_true", help="Output in JSON format")
    parser.add_argument("-d", "--daemon", action="store_true", help="Run the app as a daemon")
    parser.add_argument("-l", "--limit", type=int, help="Limit number of subnets displayed")

    args = parser.parse_args()

    if args.daemon:
        daemonize()
    elif args.subnet and args.prefix:
        message, subnets = subnet_ipv6(args.subnet, args.prefix, args.limit)

if message.get("error"):
    print(f"Error: {message['error']}")
    sys.exit(1)  # Exit with error code

output_text = f"\nGenerated {message['total_subnets']} subnets, displaying {len(subnets)}:\n"
if message.get("warning"):
    output_text += f"\n{message['warning']}\n"

output_text += "\n".join(str(subnet) for subnet in subnets)

if args.output:
    with open(args.output, "w") as file:
        file.write(output_text)
    print(f"Subnets written to {args.output}")
else:
    print(output_text)