import random
import re
import urllib2

PRIVATE_ADDRESS = re.compile(r"^(" + '|'.join([
    r"127\.\d{1,3}\.\d{1,3}\.\d{1,3}", # PRIV_LOC
    r"10\.\d{1,3}\.\d{1,3}\.\d{1,3}", # PRIV_24
    r"192\.168\.\d{1,3}.\d{1,3}", # PRIV_20
    r"172.(1[6-9]|2[0-9]|3[0-1]).[0-9]{1,3}.[0-9]{1,3}" # PRIV_16
]) + r")$")


def is_ip_private(ip):
    ''' Check id an IPv4 address is private.
  
    This function uses a regular expression to Check
    if a IPv4 address is private.
    
    - **parameters**, **types**, **return** and **return types**::
      :param ip: an IPV4 address
      :type ip: string
      :return: return None if the address is private and _sre.SRE_Match if it is
      :rtype: None or _sre.SRE_Match
    '''
    return PRIVATE_ADDRESS.match(ip)


def generate_addresses(n):
    addresses = set([])
    while len(addresses) is not n:
      address = '.'.join(str(random.randrange(256)) for _ in range(4))
      if not is_ip_private(address):
        addresses.add(address)
    return addresses


def generate_urls(n, scheme='http', path='/'):
    return ("{}://{}{}".format(scheme, address, path) for address in generate_addresses(n))


def is_live(url, timeout=5):
    try:
        return urllib2.urlopen(url, timeout=timeout).getcode()
    except urllib2.URLError, e:
        return False
    
    
def scan(n, timeout=1, **kwargs):
    for url in generate_urls(n, **kwargs):
       print is_live(url, timeout=timeout)

scan(100)

