# IPv6-subnet-planner "webapp"

Crude attempt to "webify" this thing.

## Features:
* Web Interface – Users can enter an IPv6 prefix and subnet size via a form.
* API Endpoint – `/api/subnet` allows programmatic access to subnetting via GET parameters.
* Validation – Prevents invalid inputs and provides useful warnings.
* JSON Output – The API returns JSON formatted subnets.

## Install:
* Install Flask:
`pip3 install flask`

Save the script as `app.py`, create a templates folder, and place index.html inside.

## Run:
`python app.py`

Open http://[::1]:5000/ in a local browser.

## Best practice
Wrap this thing in nginx and add an SSL certificate.