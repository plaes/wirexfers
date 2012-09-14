# -*- coding: utf-8 -*-
"""
wirexfers.protocols.ipizza
~~~~~~~~~~~~~~~~~~~~~~~~~~

IPizza protocol implementations.
"""
from time import time
from base64 import b64encode

from Crypto.Hash import SHA
from Crypto.Signature import PKCS1_v1_5

from . import KeyChainBase, ProviderBase

class IPizzaKeyChain(KeyChainBase):

    def __init__(self, private_key, public_key):
        #: RSA private key (:py:class:`Crypto.PublicKey.RSA._RSAobj`) object.
        #: See :func:`wirexfers.utils.load_key`.
        self.private_key = private_key

        ##: Private key password
        #self.private_pass = private_pass

        #: RSA public key (:py:class:`Crypto.PublicKey.RSA._RSAobj`) object
        #: See :func:`wirexfers.utils.load_key`.
        self.public_key = public_key

class IPizzaProviderBase(ProviderBase):
    """Base class for IPizza protocol provider."""

    def _sign_request(self, info, return_urls):
        """Create and sign payment request data."""
        # Basic fields
        fields = [('VK_SERVICE', u'1002'),
                  ('VK_VERSION', u'008'),
                  ('VK_SND_ID',  self.user),
                  ('VK_STAMP',   '%d' % int(time())),
                  ('VK_AMOUNT',  info.amount),
                  ('VK_CURR',    u'EUR'),
                  ('VK_REF',     info.refnum),
                  ('VK_MSG',     info.message)]

        ## MAC calculation for request 1002
        mac_fields = ('SERVICE', 'VERSION', 'SND_ID', \
                      'STAMP', 'AMOUNT', 'CURR', 'REF', 'MSG')
        f = lambda x: dict(fields).get('VK_%s' % x)

        # MAC field: ordered fields and their lengths: e.g., '003one003two'
        mac = u''.join(map(lambda k: '%03d%s' % (len(f(k)), f(k)), mac_fields))
        # Append extra fields
        fields.append(('VK_MAC', b64encode( \
                    PKCS1_v1_5.new(self.keychain.private_key).sign(SHA.new(mac)))))
        fields.append(('VK_RETURN', return_urls['return']))
        return fields
