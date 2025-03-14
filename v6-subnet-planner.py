#!/usr/bin/env python3
import ipaddress
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
    ipv6_prefix = input("Enter the IPv6 prefix (e.g., 3fff:1::/32): ")
    new_prefix = int(input("Enter the new subnet prefix length (e.g., 48): "))
    
    subnets = subnet_ipv6(ipv6_prefix, new_prefix)
    
    if subnets:
        print(f"\nGenerated {len(subnets)} subnets:")
        for subnet in subnets:
            print(subnet)
    else:
        print("No subnets generated.")

if __name__ == "__main__":
    main()

