#!/usr/bin/env python


"""Find random web servers on the net.

------------
How it works
------------

* Generate a random non private IPv4 address.
* Convert that address into a URL.
* Use urllib2's getcode method to check if the url is live.
"""

import random
import re
import urllib2
import sys

# This regular expression is used to eliminate private addresses.
PRIVATE_ADDRESS = re.compile(r"^(" + '|'.join([
    r"127\.\d{1,3}\.\d{1,3}\.\d{1,3}", # PRIV_LOC
    r"10\.\d{1,3}\.\d{1,3}\.\d{1,3}", # PRIV_24
    r"192\.168\.\d{1,3}.\d{1,3}", # PRIV_20
    r"172.(1[6-9]|2[0-9]|3[0-1]).[0-9]{1,3}.[0-9]{1,3}" # PRIV_16
]) + r")$")


def is_ip_private(address):
    ''' Check id an IPv4 address is private.

    This function uses a regular expression to Check
    if a IPv4 address is private.

    - **parameters**, **types**, **return** and **return types**::
      :param address: an IPV4 address
      :type address: string
      :return: return None if the address is private and _sre.SRE_Match if it is
      :rtype: None or _sre.SRE_Match
    '''
    return PRIVATE_ADDRESS.match(address)

def generate_address():
    result = []
    while len(result) is not 1:
        address = '.'.join(str(random.randrange(256)) for _ in range(4))
        if is_ip_private(address):
            pass
        else:
            result.append(address)
    return result.pop()
    

def generate_url(scheme='http', path='/'):
    return "{}://{}{}".format(scheme, generate_address(), path)

def is_live(url, timeout=0.203097):
    """Check if a URL is live.

    This function uses urllib2's getcode method to check
    if a URL is live.

    **parameters**
    :param url: The url to check.
    :param timeout: How long to wait for a connection, the default is 3 seconds
    :type url: string
    :type timeout: int or float
    :rtype: bool
    """
    try:
        if urllib2.urlopen(url, timeout=timeout).getcode() is 200:
            return True
        else:
            return False
    except KeyboardInterrupt:
        sys.stdout.write('\r\n')
        answer = raw_input("Are you sure you want to quit? [y, n] : ")
        if 'y' in answer:
            sys.stdout.write('\r\n')
            sys.exit(0)
    except Exception:
        return False

def scan(amount):
    live_urls = set([])
    while len(live_urls) is not amount:
        url = generate_url()
        if is_live(url):
            print url
            live_urls.add(url)
    return live_urls

scan(10)