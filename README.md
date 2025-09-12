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

To run (Updates every hour by default) from PowerShell go to the folder holding your files and run. This will rerun the script every hour. I could have set this as a scheduled task but I wanted to be able to constantly view any updates. I may change this in the future.
```sh
./check.ps1
```

Every hour it will rerun and look for any changes in the data.

## Optional (Website)
I did this the easy way. Install IIS on my hosted server and set the Default Web Site to point at where all these files are held. You can then browse to the website and get a nicely formatted output of the check.ps1 script.

