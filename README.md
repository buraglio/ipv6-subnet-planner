# IPv6 Subnet Planner

## Description

The IPv6 Subnet Planner is nothing more than a simple Python script designed to help network engineers, IT administrators, or zealous hobbiests lan and allocate IPv6 subnets. It really just takes an IPv6 prefix as input and generates subnets of a user-specified prefix length. This can be useful for visualizing the subnets and for importing them into other things for more effective use.

## "Features"

Accepts an IPv6 prefix and a new prefix length to generate subnet allocations.

Allows output to be saved to a file.

## Requirements

Python 3.x

## Installation

Ensure you have Python installed, then download the script. Profit (maybe, but not likely).

## Use

Run the script using the command line with the following options:

`chmod +x v6_subnet_planner.py`

`./v6_subnet_planner.py -s <IPv6 Prefix> -p <New Prefix Length> [-o <Output File>]`

Arguments

* -s, --subnet (Required): The IPv6 prefix to be subnetted (e.g., 3fff:1::/32).

* -p, --prefix (Required): The nwe subnet prefix length (e.g., 48).

* -o, --output (Optional): The output file to save the generated subnets.

* -j, --json (Optional): Output to JSON format.

Example

`./v6_subnet_planner.py -s 3fff:1::/32 -p 48 -o subnets.txt`

This command will generate /48 subnets from the given /32 prefix and save them to subnets.txt.