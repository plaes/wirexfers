# -*- coding: utf-8 -*-
"""
wirexfers.protocols.tupas
~~~~~~~~~~~~~~~~~~~~~~~~~

Solo (TUPAS) protocol implementations.
"""
from time import time

from Crypto.Hash import MD5

from . import KeyChainBase, ProviderBase
from .. import PaymentResponse
from ..exc import InvalidResponseError

# Currently only single bank implemented, therefore no generic TUPAS/Solo
# protocol implementation available.

def MAC_hash(mac_str):
    """
    Returns MAC hash value in uppercase hexadecimal form and truncated to
    32 characters.
    """
    return MD5.new(mac_str).hexdigest().upper()[:32]

class SoloKeyChain(KeyChainBase):

    def __init__(self, mac_key):
        #: MAC key provided by bank, used for signing and verifying payment data
        self.mac_key = mac_key

class NordeaEEProvider(ProviderBase):
    """
    | Nordea Bank Finland Plc Eesti / AS Nordea Finance Estonia
    | https://www.nordea.ee

    Protocol
        Solo/TUPAS
    KeyChain
        :class:`~.SoloKeyChain`
    Supported return urls:
        * ``cancel`` - user cancels payment
        * ``reject`` - bank rejects payment (due to insufficient funds, ...)
        * ``return`` - payment is successful

    Supported protocol version:
        * ``0003``
    """

    # TODO: protocol versions: 0004
    # TODO: CONFIRM
    # TODO: handle payment date (currently only EXPRESS is used)
    # TODO: handle different receiver/account
    # TODO: handle language
    # TODO: make signing algorithm configurable

    def _sign_request(self, payment, return_urls):
        """Create and sign payment request data."""
        fields = [('VERSION', u'0003'),
                  ('STAMP', u'%d' % int(time())),
                  ('RCV_ID', self.user),
                  # RCV_ACCOUNT    (optional)
                  # RCV_NAME       (optional)
                  ('LANGUAGE', u'4'),
                  ('AMOUNT', payment.amount),
                  ('REF', payment.refnum),
                  # TAX_CODE (becomes mandatory in version 0004)
                  ('DATE', u'EXPRESS'),
                  ('MSG', payment.message),
                  ('RETURN', return_urls['return']),
                  ('CANCEL', return_urls['cancel']),
                  ('REJECT', return_urls['reject']),
                  ('CONFIRM', u'YES'),
                  ('KEYVERS', u'0001'),
                  ('CUR', u'EUR')]
        # MAC calculation
        f = lambda x: dict(fields).get(x)
        k = ('VERSION', 'STAMP', 'RCV_ID', 'AMOUNT', 'REF', 'DATE', 'CUR')
        m = '%s&%s&' % ('&'.join(map(f, k)), self.keychain.mac_key)
        fields.append(('MAC', MAC_hash(m)))
        return fields

    def parse_response(self, form, success=False):
        """Parse and return payment response."""
        # MAC calculation
        f = lambda x: form.get('RETURN_%s' % x, '')
        k = ('VERSION', 'STAMP', 'REF', 'PAID')
        m = '%s&%s&' % ('&'.join(map(f, k)), self.keychain.mac_key)
        if MAC_hash(m) != form.get('RETURN_MAC'):
            raise InvalidResponseError
        # Save worthwhile data from the response
        data = {}
        for key in ('REF', 'PAID'):
            item = data.get('RETURN_%s' % key, None)
            if item != None:
                data[key] = item
        return PaymentResponse(self, data, success)
