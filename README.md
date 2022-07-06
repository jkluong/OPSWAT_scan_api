# OPSWAT_scan_api
program to scan a file using OPSWAT

kept it quick and simple for the assignment. 
could improve in the following ways:
  use helper functions to clean up the code
  store main url in a constant so that it can be changed when version changes or url changes
  use a proper way of limiting api calls to check for scan completion or even better using webhooks

Requires Python 3.10 and pip. Also requires the requests package.

pip install requests

Usage: python scan.py file_to_be_scanned api_key
