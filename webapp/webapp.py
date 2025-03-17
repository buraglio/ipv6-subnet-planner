#!/usr/bin/env python3
#Create a flask app that exposes an API
from flask import Flask, request, render_template, jsonify
import ipaddress

app = Flask(__name__)

def subnet_ipv6(prefix: str, new_prefix: int):
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

if __name__ == "__main__":
    app.run(debug=True)
