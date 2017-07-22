
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


def generate_addresses(amount):
    """ Generate a set list of random IPv4 addresses.

    **parameters**
    :param amount: The number of addresses to generate.
    :type amount: int
    :return: a set list of random IPv4 addresses.
    :rtype: set
    """
    addresses = set([])
    while len(addresses) is not amount:
        address = '.'.join(str(random.randrange(256)) for _ in range(4))
        if not is_ip_private(address):
            addresses.add(address)
    return addresses


def generate_urls(amount, scheme='http', path='/'):
    """ Generate a list of random URL's.

    **parameters**
    :param amount: The number of URL's to generate.
    :param scheme: the url scheme to use, the default scheme is http.
    :param path: the url path to use, default is "/" aka root
    :rtype: generator
    """
    return ("{}://{}{}".format(scheme, address, path) for address in generate_addresses(amount))


def is_live(url, timeout=3):
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
            return
        else:
            return False
    except urllib2.URLError:
        return False


def scan(amount, timeout=1, **kwargs):
    for url in generate_urls(amount, **kwargs):
        if is_live(url, timeout=timeout):
            print url

if __name__ == '__main__':
    scan(100)
