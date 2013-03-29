#!/usr/bin/env python2
import os
import re
import sys
import httplib
from urllib import urlencode
from urllib2 import urlopen
from argparse import ArgumentParser
from collections import OrderedDict

def _discover_own_ipv4(ipv4_discover_url):
    response = urlopen(ipv4_discover_url)
    code, content = response.code, response.read()
    if code != httplib.OK:
        print >>sys.stderr, 'error: could not discover own ipv4 address.'
        print >>sys.stderr, 'server returned {}, {}'.format(code, content)
        raise SystemExit(1)
    parsed_response = re.search(r'Your IP address is\s*:\s*(?P<ipv4_address>\d+\.\d+\.\d+\.\d+)', content)
    if parsed_response is None:
        print >>sys.stderr, 'error: could not parse own ipv4 properly'
        print >>sys.stderr, 'server returned:', content
        raise SystemExit(2)
    return parsed_response.groupdict()['ipv4_address']
    
def _update_ipv4(hostname, password, update_url, ipv4_address):
    data = urlencode(OrderedDict(hostname=hostname, password=password, myip=ipv4_address))
    response = urlopen(update_url, data)
    content = response.read().strip()
    if response.code != httplib.OK:
        print >>sys.stderr, 'error: update failed. error is {}'.format(response.code)
        print >>sys.stderr, content
        raise SystemExit(3)
    parsed_content = re.match(r'^(?P<key>badauth|nochg|good)(\s(?P<value>.*))?$', content)
    if parsed_content is None:
        print >>sys.stderr, 'error: unknown returned response: {}'.format(content)
        raise SystemExit(4)
    key, value = parsed_content.groupdict()['key'], parsed_content.groupdict()['value']
    if key == 'badauth':
        print >>sys.stderr, 'error: the domain name and password do not match'
        print >>sys.stderr, 'Make sure you are using a domain name that has been marked for dynamic updates,'
        print >>sys.stderr, 'and that the password used is the update key (not your account password).'
        raise SystemExit(5)
    elif key == 'nochg':
        print >>sys.stderr, 'no update required (ipv4 is {})'.format(value)
    elif key == 'good':
        print >>sys.stderr, 'update complete: {}'.format(value)

def main():
    parser = ArgumentParser()
    parser.add_argument('hostname', help='The hostname (domain name) to be updated. Make sure this domain has been marked for dynamic DNS updating')
    parser.add_argument('password', help='Update key for this domain (as generated from the zone management interface)')
    parser.add_argument('-u', '--update-url', default='https://dyn.dns.he.net/nic/update',
                        help='URL to post the update to')
    parser.add_argument('-d', '--ipv4-discover-url', default='http://checkip.dns.he.net',
                        help='Service for discovery of own IPv4 address')
    parser.add_argument('-i', '--ipv4-address', default=None,
                        help='The IPv4 address to be updated for this domain. Leave blank to auto-discover')
    args = parser.parse_args()

    if args.ipv4_address is None:
        args.ipv4_address = _discover_own_ipv4(args.ipv4_discover_url)

    _update_ipv4(args.hostname, args.password, args.update_url, args.ipv4_address)

if __name__ == '__main__':
    main()
