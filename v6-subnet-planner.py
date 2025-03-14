#!/usr/bin/env python3
# Create a subnet list for IPv6 address planning. 
# This does not support IPv4 because it is a dead language.
# Hastily cobbled together by buraglio@forwardingplane.net
# Licensed as open with attribution
# Currently there are issues with generating from longer prefixes that I have not figured out, sorry
import ipaddress
import argparse
import json

def subnet_ipv6(prefix: str, new_prefix: int):
    try:
        network = ipaddress.IPv6Network(prefix, strict=False)
        if new_prefix <= network.prefixlen:
            print("Error: New prefix must be larger than the original prefix.")
            return []
        
        subnets = list(network.subnets(new_prefix=new_prefix))
        
        if new_prefix % 4 != 0:
            print("Warning: This will not output prefixes on a nibble boundary. Maybe rethink what you are doing?")
        
        return subnets
    except ValueError as e:
        print(f"Invalid input: {e}")
        return []

def main():
    parser = argparse.ArgumentParser(description="IPv6 Subnet Planner")
    parser.add_argument("-s", "--subnet", required=True, help="IPv6 prefix (e.g., 3fff:1::/32)")
    parser.add_argument("-p", "--prefix", type=int, required=True, help="New subnet prefix length (e.g., 48)")
    parser.add_argument("-o", "--output", help="Output file name")
    parser.add_argument("-j", "--json", action="store_true", help="Output in JSON format")
    
    args = parser.parse_args()
    
    subnets = subnet_ipv6(args.subnet, args.prefix)
    
    if subnets:
        if args.json:
            output_data = {"subnets": [str(subnet) for subnet in subnets]}
            output_text = json.dumps(output_data, indent=4)
        else:
            output_text = f"\nGenerated {len(subnets)} subnets:\n" + "\n".join(str(subnet) for subnet in subnets)
        
        if args.output:
            with open(args.output, "w") as file:
                file.write(output_text)
            print(f"Subnets written to {args.output}")
        else:
            print(output_text)
    else:
        print("No subnets generated.")

if __name__ == "__main__":
    main()
