update_he_dns.py
================

    usage: update_he_dns.py [-h] [-u UPDATE_URL] [-d IPV4_DISCOVER_URL]
                            [-i IPV4_ADDRESS]
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
      -d IPV4_DISCOVER_URL, --ipv4-discover-url IPV4_DISCOVER_URL
                            Service for discovery of own IPv4 address
      -i IPV4_ADDRESS, --ipv4-address IPV4_ADDRESS
                            The IPv4 address to be updated for this domain. Leave
                            blank to auto-discover
