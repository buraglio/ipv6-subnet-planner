#!/usr/bin/env python3
import ipaddress
import argparse
# Keep it super simple and use easy modules because I'm dumb
# Takes a STD input of a prefix (3fff:1::/32) and breaks it into a user defined set of subnets

def subnet_ipv6(prefix: str, new_prefix: int):
    try:
        network = ipaddress.IPv6Network(prefix, strict=False)
        if new_prefix <= network.prefixlen:
            print("Error: New prefix must be larger than the original prefix.")
            return []
        
        subnets = list(network.subnets(new_prefix=new_prefix))
        return subnets
    except ValueError as e:
        print(f"Invalid input: {e}")
        return []

def main():
    parser = argparse.ArgumentParser(description="IPv6 Subnet Planner")
    parser.add_argument("-s", "--subnet", required=True, help="IPv6 prefix (e.g., 2001:db8::/32)")
    parser.add_argument("-p", "--prefix", type=int, required=True, help="New subnet prefix length (e.g., 48)")
    parser.add_argument("-o", "--output", help="Output file name")
    
    args = parser.parse_args()
    
    subnets = subnet_ipv6(args.subnet, args.prefix)
    
    if subnets:
        output_text = f"\nGenerated {len(subnets)} subnets:\n" + "\n".join(str(subnet) for subnet in subnets)
        print(output_text)
        
        if args.output:
            with open(args.output, "w") as file:
                file.write(output_text)
            print(f"Subnets written to {args.output}")
    else:
        print("No subnets generated.")

if __name__ == "__main__":
    main()


