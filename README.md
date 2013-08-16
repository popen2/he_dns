update_he_dns.py
================

    usage: update_he_dns.py [-h] [-u UPDATE_URL] [-d DISCOVER_URL] [-t TYPE]
                            [-i IP_ADDRESS]
                            hostname password
    
    positional arguments:
      hostname              The hostname (domain name) to be updated. Make sure
                            this domain has been marked for dynamic DNS updating
      password              Update key for this domain (as generated from the zone
                            management interface)
    
    optional arguments:
      -h, --help            show this help message and exit
      -u UPDATE_URL, --update-url UPDATE_URL
                            URL to post the update to
      -d DISCOVER_URL, --discover-url DISCOVER_URL
                            Service for discovery of own address
      -t TYPE, --type TYPE  Type of update: either "4" for IPv4 or "6" for IPv6
      -i IP_ADDRESS, --ip-address IP_ADDRESS
                            The IP address to be updated for this domain. Leave
                            blank to auto-discover
