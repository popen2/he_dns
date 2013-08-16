#!/usr/bin/env python
import os
import re
import sys
import socket
import httplib
import urlparse
from urllib import urlencode
from urllib2 import urlopen
from argparse import ArgumentParser
from collections import OrderedDict

def _get_discover_url(given_discover_url, update_type):
    if update_type == '4':
        return given_discover_url
    elif update_type == '6':
        parsed_url = urlparse.urlsplit(given_discover_url)
        for (family, socktype, proto, canonname, sockaddr) in socket.getaddrinfo(parsed_url.netloc, parsed_url.port, socket.AF_INET6):
            address, port, flow_info, scope_id = sockaddr
            return urlparse.urlunsplit((parsed_url.scheme, '[' + address + ']', parsed_url.path, parsed_url.query, parsed_url.fragment))
        raise ValueError('Cannot find an IPv6 address with the discovery URL {}'.format(given_discover_url))
    else:
        raise ValueError('Unknown update type {!r}'.format(update_type))

def _discover_own_address(discover_url):
    response = urlopen(discover_url)
    code, content = response.code, response.read()
    if code != httplib.OK:
        print >>sys.stderr, 'error: could not discover own address.'
        print >>sys.stderr, 'server returned {}, {}'.format(code, content)
        raise SystemExit(1)
    parsed_response = re.search(r'Your IP address is\s*:\s*(?P<ip_address>(\d+\.\d+\.\d+\.\d+)|([0-9a-fA-F:]+))', content)
    if parsed_response is None:
        print >>sys.stderr, 'error: could not parse own IP properly'
        print >>sys.stderr, 'server returned:', content
        raise SystemExit(2)
    return parsed_response.groupdict()['ip_address']
    
def _send_update(hostname, password, update_url, ip_address):
    data = urlencode(OrderedDict(hostname=hostname, password=password, myip=ip_address))
    response = urlopen(update_url, data)
    content = response.read().strip()
    if response.code != httplib.OK:
        print >>sys.stderr, 'error: update failed. error is {}'.format(response.code)
        print >>sys.stderr, content
        raise SystemExit(3)
    parsed_content = re.match(r'^(?P<key>badauth|nochg|good|noipv6)(\s(?P<value>.*))?$', content)
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
        print >>sys.stderr, 'no update required (IP is {})'.format(value)
    elif key == 'noipv6':
        print >>sys.stderr, 'cannot update ipv6 for this hostname'
    elif key == 'good':
        print >>sys.stderr, 'update complete: {}'.format(value)

def main():
    parser = ArgumentParser()
    parser.add_argument('hostname', help='The hostname (domain name) to be updated. Make sure this domain has been marked for dynamic DNS updating')
    parser.add_argument('password', help='Update key for this domain (as generated from the zone management interface)')
    parser.add_argument('-u', '--update-url', default='https://dyn.dns.he.net/nic/update',
                        help='URL to post the update to')
    parser.add_argument('-d', '--discover-url', default='http://checkip.dns.he.net',
                        help='Service for discovery of own address')
    parser.add_argument('-t', '--type', default='4',
                        help='Type of update: either "4" for IPv4 or "6" for IPv6')
    parser.add_argument('-i', '--ip-address', default=None,
                        help='The IP address to be updated for this domain. Leave blank to auto-discover')
    args = parser.parse_args()

    if args.ip_address is None:
        discover_url = _get_discover_url(args.discover_url, args.type)
        args.ip_address = _discover_own_address(discover_url)

    _send_update(args.hostname, args.password, args.update_url, args.ip_address)

if __name__ == '__main__':
    main()
