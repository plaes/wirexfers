# -*- coding: utf-8 -*-
"""
wirexfers.protocols.ipizza
~~~~~~~~~~~~~~~~~~~~~~~~~~

IPizza protocol implementations.
"""
from time import time
from base64 import b64encode, b64decode

from Crypto.Hash import SHA
from Crypto.Signature import PKCS1_v1_5

from . import KeyChainBase, ProviderBase
from .. import PaymentResponse
from ..exc import InvalidResponseError

class IPizzaKeyChain(KeyChainBase):

    def __init__(self, private_key, public_key):
        #: RSA private key (:py:class:`Crypto.PublicKey.RSA._RSAobj`) object.
        #: See :func:`wirexfers.utils.load_key`.
        self.private_key = private_key

        #: RSA public key (:py:class:`Crypto.PublicKey.RSA._RSAobj`) object
        #: See :func:`wirexfers.utils.load_key`.
        self.public_key = public_key

class IPizzaProviderBase(ProviderBase):
    """Base class for IPizza protocol provider.

    Protocol
        IPizza
    KeyChain
        :class:`~.IPizzaKeyChain`
    Supported return urls:
        * ``return``
    Supported protocol version:
        * ``008``
    """

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

        # Check whether provider supplies extra fields
        if hasattr(self, 'extra_fields'):
            fields.extend(self.extra_fields)

        ## MAC calculation for request 1002
        mac_fields = ('SERVICE', 'VERSION', 'SND_ID', \
                      'STAMP', 'AMOUNT', 'CURR', 'REF', 'MSG')
        f = lambda x: dict(fields).get('VK_%s' % x)

        # MAC field: ordered fields and their lengths: e.g., '003one003two'
        mac = u''.join(map(lambda k: '%03d%s' % (len(f(k).encode('utf-8')), f(k)), mac_fields)).encode('utf-8')
        # Append mac fields
        fields.append(('VK_MAC', b64encode( \
                    PKCS1_v1_5.new(self.keychain.private_key)
                              .sign(SHA.new(mac)))))
        fields.append(('VK_RETURN', return_urls['return']))
        return fields

    def parse_response(self, form):
        """Parse and return payment response."""
        fields = {
            # Successful payment
            '1101': ('SERVICE', 'VERSION', 'SND_ID', 'REC_ID', 'STAMP', #  1..5
                     'T_NO', 'AMOUNT', 'CURR', 'REC_ACC', 'REC_NAME',   #  6..10
                     'SND_ACC', 'SND_NAME', 'REF', 'MSG', 'T_DATE'),    # 11..15
            # Unsuccessful payment
            '1901': ('SERVICE', 'VERSION', 'SND_ID', 'REC_ID', 'STAMP', #  1..5
                     'REF', 'MSG')                                      #  6..7
        }
        # See which response we got
        resp = form.get('VK_SERVICE', None)
        if not resp and resp not in fields:
            raise InvalidResponseError
        success = resp == '1101'
        # Parse and validate MAC
        f = lambda x: form.get('VK_%s' % x)
        m = u''.join(map(lambda k: '%03d%s' % (len(f(k).encode('utf-8')), f(k)), fields[resp])).encode('utf-8')
        if not PKCS1_v1_5.new(self.keychain.public_key) \
                         .verify(SHA.new(m), b64decode(f('MAC'))):
            raise InvalidResponseError
        # Save payment data
        data = {}
        if success:
            for item in ('T_NO', 'AMOUNT', 'CURR', 'REC_ACC', 'REC_NAME',
                         'SND_ACC', 'SND_NAME', 'REF', 'MSG', 'T_DATE'):
                data[item] = f(item)
        return PaymentResponse(self, data, success)

class LHVEEProvider(IPizzaProviderBase):
    """
    | AS LHV Pank
    | https://www.lhv.ee

    Protocol
        IPizza
    KeyChain
        :class:`~.IPizzaKeyChain`
    Supported return urls:
        * ``return``
    Supported protocol version:
        * ``0003``
    """
    extra_fields = (('VK_CHARSET', 'UTF-8'),)

class SEBEEProvider(IPizzaProviderBase):
    """
    | AS SEB Pank
    | http://www.seb.ee

    Protocol
        IPizza
    KeyChain
        :class:`~.IPizzaKeyChain`
    Supported return urls:
        * ``return``
    Supported protocol version:
        * ``0003``
    """
    extra_fields = (('VK_CHARSET', 'UTF-8'),)

class SwedBankEEProvider(IPizzaProviderBase):
    """
    | SWEDBANK AS
    | https://www.swedbank.ee

    Protocol
        IPizza
    KeyChain
        :class:`~.IPizzaKeyChain`
    Supported return urls:
        * ``return``
    Supported protocol version:
        * ``0003``
    """
    extra_fields = (('VK_ENCODING', 'UTF-8'),)
