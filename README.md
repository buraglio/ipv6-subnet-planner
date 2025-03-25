# Python IPv6 Subnet Planner

## Description

The IPv6 Subnet Planner is nothing more than a simple Python script designed to help network engineers, IT administrators, or zealous hobbyists to plan and allocate IPv6 subnets. It really just takes an IPv6 prefix as input and generates subnets of a user-specified prefix length. This can be useful for visualizing the subnets and for importing them into other things for more effective use. 

It does have some limits. If you ask the script to compile all of the /127 prefixes in a /64, be prepared to wait a pretty long time. It is best used to do high level planning from RIR allocations or PA allocations at an organizational level (i.e. break a /32 into a bunch of /40s). It assumes you want to do things from the CLI, but someone could probably write this into a web app, maybe. 

## "Features"

* Accepts an IPv6 prefix and a new prefix length to generate subnet allocations.

* Allows output to be saved to a file.

* Warns if the prefixes requested are not on a nibble boundary.

* Outputs to json if requested. Why? I have no idea but it was shockingly easy to do. 

## Requirements

Python 3.x

## Installation

Ensure you have Python installed, then download the script.

Install all requirements:
`pip3 install flask gunicorn argparse`
Profit (maybe, but not likely).

~Optional:~

Set up a venv (not required. These things drive me nuts but I am beginning to see utility)
cd to the directory where you want to run this thing. 
`python3 -m venv .`
`source bin/activate`
`python3 -m pip install flask gunicorn argparse`

## Use

Run the script using the command line with the following options:

`chmod +x v6_subnet_planner.py`

`./v6_subnet_planner.py -s <IPv6 Prefix> -p <New Prefix Length> [-o <Output File>]`

Arguments

* -s, --subnet (Required): The IPv6 prefix to be subnetted (e.g., 3fff:1::/32).

* -p, --prefix (Required): The new subnet prefix length (e.g., 48).

* -o, --output (Optional): The output file to save the generated subnets.

* -j, --json (Optional): Output to JSON format.

* -l, --limit (Optional): Limit output to a specific number of lines (it will still fully process, this is cosmetic only)

Example

`./v6_subnet_planner.py -s 3fff:1::/32 -p 48 -l 4 -o subnets.txt`

This command will generate /48 subnets from the given /32 prefix and save the first 4 of them to subnets.txt.

# Webapp

## IPv6-subnet-planner "webapp"

Crude attempt to "webify" this thing.

## Features:
* Web Interface – Users can enter an IPv6 prefix and subnet size via a form.
* API Endpoint – `/api/subnet` allows programmatic access to subnetting via POST parameters.
* Validation – Prevents invalid inputs and provides questionably useful warnings.
* JSON Output – The API returns messy JSON formatted subnets.

## Install:
* Install Flask:
`pip3 install flask gunicorn argparse`

Save the script as `v6-subnet-planner.py`.
`chmod +x v6-subnet-planner.py`

## Run:
`python v6-subnet-planner.py -d`
or
`./v6-subnet-planner.py -d`

Running with `-d` requires `argparse` and will run this in the background using `gunicorn`. It will run as normal without `-d`

Open http://[::1]:5000/ in a local browser.

## Best practice
Wrap this thing in nginx and add an SSL certificate.

## To Do
* Make an init or systemctl script to start this piece of junk on boot
* Add option to output as plan text as well as json

