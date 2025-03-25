#!/usr/bin/env python3
# Create a subnet list for IPv6 address planning. 
# This does not support IPv4 because it is a dead language.
# Hastily cobbled together by buraglio@forwardingplane.net
# Licensed as open with attribution
# Currently there are issues with generating from longer prefixes that I have not figured out, sorry
import ipaddress
import argparse
import json
import sys
import os
import time
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

def subnet_ipv6(prefix: str, new_prefix: int):
    """Generate subnets from an IPv6 prefix."""
    try:
        network = ipaddress.IPv6Network(prefix, strict=False)
        if new_prefix <= network.prefixlen:
            return {"error": "New prefix must be larger than the original prefix.", "total_subnets": 0}, []
        
        subnets = list(network.subnets(new_prefix=new_prefix))

        warning = None
        if new_prefix % 4 != 0:
            warning = "Warning: This will not output prefixes on a nibble boundary."

        return {"warning": warning, "total_subnets": len(subnets)}, subnets

    except ValueError as e:
        return {"error": f"Invalid input: {e}", "total_subnets": 0}, []

@app.route("/")
def index():
    """Serve the web form."""
    return render_template("index.html")

@app.route("/api/subnet", methods=["POST"])
def api_subnet():
    """API endpoint to generate subnets via POST requests from the web form."""
    
    prefix = request.form.get("subnet")
    new_prefix = request.form.get("prefix")
    limit = request.form.get("limit", type=int)  # Get limit from form input

    if not prefix or not new_prefix or not new_prefix.isdigit():
        return jsonify({"error": "Invalid input. Please enter a valid IPv6 prefix and prefix size."}), 400

    new_prefix = int(new_prefix)

    message, subnets = subnet_ipv6(prefix, new_prefix)

    if "error" in message:
        return jsonify({"error": message["error"]}), 400

    # Apply limit to web response if provided
    display_subnets = subnets[:limit] if limit else subnets

    return jsonify({
        "warning": message.get("warning"),
        "total_subnets": message["total_subnets"],
        "subnets_shown": len(display_subnets),
        "subnets": [str(subnet) for subnet in display_subnets]
    })

def run_flask():
    """Start the Flask web server."""
    app.run(host="::1", port=5000, debug=False)

def daemonize():
    """Fork the process to run in the background as a daemon."""
    try:
        pid = os.fork()
        if pid > 0:
            # Exit parent process
            sys.exit(0)
    except OSError as e:
        print(f"Fork #1 failed: {e}")
        sys.exit(1)

    os.setsid()

    try:
        pid = os.fork()
        if pid > 0:
            # Exit second parent process
            sys.exit(0)
    except OSError as e:
        print(f"Fork #2 failed: {e}")
        sys.exit(1)

    # Redirect standard file descriptors to /dev/null
    sys.stdout.flush()
    sys.stderr.flush()
    with open("/dev/null", "rb") as f:
        os.dup2(f.fileno(), sys.stdin.fileno())
    with open("/dev/null", "ab") as f:
        os.dup2(f.fileno(), sys.stdout.fileno())
        os.dup2(f.fileno(), sys.stderr.fileno())

    # Run the Flask app in the background
    run_flask()

def main():
    parser = argparse.ArgumentParser(description="IPv6 Subnet Planner")
    parser.add_argument("-s", "--subnet", help="IPv6 prefix (e.g., 3ffe:1::/32)")
    parser.add_argument("-p", "--prefix", type=int, help="New subnet prefix length (e.g., 48)")
    parser.add_argument("-o", "--output", help="Output file name")
    parser.add_argument("-j", "--json", action="store_true", help="Output in JSON format")
    parser.add_argument("-l", "--limit", type=int, help="Limit the number of displayed subnets")
    parser.add_argument("-d", "--daemon", action="store_true", help="Run the web app as a daemon")

    args = parser.parse_args()

    if args.daemon:
        print("Starting web app in daemon mode...")
        daemonize()
        return

    if args.subnet and args.prefix:
        message, subnets = subnet_ipv6(args.subnet, args.prefix)

        if message.get("error"):
            print(f"Error: {message['error']}")
            sys.exit(1)

        # Apply limit only to CLI output
        display_subnets = subnets[:args.limit] if args.limit else subnets

        if args.json:
            output_data = {
                "warning": message.get("warning"),
                "total_subnets": message["total_subnets"],
                "subnets_shown": len(display_subnets),
                "subnets": [str(subnet) for subnet in display_subnets]
            }
            output_text = json.dumps(output_data, indent=4)
        else:
            output_text = f"\nGenerated {message['total_subnets']} subnets"
            if args.limit:
                output_text += f", displaying {len(display_subnets)}:\n"
            else:
                output_text += ":\n"

            if message.get("warning"):
                output_text += f"\n{message['warning']}\n"

            output_text += "\n".join(str(subnet) for subnet in display_subnets)

        if args.output:
            with open(args.output, "w") as file:
                file.write(output_text)
            print(f"Subnets written to {args.output}")
        else:
            print(output_text)

    else:
        print("Error: No valid arguments provided. Use -h for help.")

if __name__ == "__main__":
    main()
