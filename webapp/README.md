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

Save the script as `webapp.py`.
`chmod +x webapp.py`

## Run:
`python app.py -d`
or
`./webapp.py -d`

Running with `-d` requires `argparse` and will run this in the background using `gunicorn`. It will run as normal without `-d`

Open http://[::1]:5000/ in a local browser.

## Best practice
Wrap this thing in nginx and add an SSL certificate.

## To Do
Make an init or systemctl script to start this piece of junk on boot