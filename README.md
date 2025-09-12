# This is a fork from https://github.com/niklaswa/tesla-order-status/tree/main

This fork is maintained by myself and has some additions. Currently these are :
- Powershell script that runs hourly and identifies and displays any changes since the initial run.
- Web front end that refreshes every 30 seconds. Nice Model 3 logo on the progress bar.

## Installation

To run the script, you need to install python3 for your operating system.

https://www.python.org/downloads/

Then you need to install the `requests` library by running:
```sh
pip install requests
```

Optional: Copy the script to a new directory, the script asks to save the tokens and order details in the current directory for reusing the tokens and for comparing the data with the last time you fetched the order details.

Then you can run the script by running:
```sh
./Check-TeslaOrderStatus.ps1
```
