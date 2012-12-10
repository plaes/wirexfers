# -*- coding: utf-8 -*-
"""
wirexfers.utils
~~~~~~~~~~~~~~~

This module provides utility functions that are used within
WireXfers, but might be also useful externally.

"""
from Crypto.PublicKey import RSA

def load_key(path, password=None):
    """Import an RSA key (private or public half).

    :param string path: path to key half.
    :param password: password for private key.
    :type password: string or None
    :rtype: :py:class:`Crypto.PublicKey.RSA._RSAobj`
    """
    with open(path, 'r') as f:
        key = RSA.importKey(f.read(), password)
        if not key:
            raise RuntimeError('Invalid key file: "%s"\n' % path)
        return key

def ref_731(n):
    """Reference number calculator. Returns reference number
    calculated using 7-3-1 algorithm used in Estonian banks.

    :param string n: base number (client id, etc)
    :rtype: string
    """
    return "%s%d" % (n,((10 - (sum(map(\
                    lambda l: int(n[-l])*(7,3,1)[(l-1) % 3], \
                    xrange(1, len(n)+1))))) % 10))
