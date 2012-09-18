# -*- coding: utf-8 -*-
"""
wirexfers.protocols.tupas
~~~~~~~~~~~~~~~~~~~~~~~~~

Solo (TUPAS) protocol implementations.
"""
from time import time

from Crypto.Hash import MD5

from . import KeyChainBase, ProviderBase

# Currently only single bank implemented, therefore no generic TUPAS/Solo
# protocol implementation available.

class SoloKeyChain(KeyChainBase):

    def __init__(self, mac_key):
        #: MAC key used for signing and verifying payment data
        self.mac_key = mac_key

class NordeaEEProvider(ProviderBase):
    """
    Nordea Bank Finland Plc Eesti/AS Nordea Finance Estonia
    http://www.nordea.ee

    Protocol: Solo/TUPAS
    KeyChain: :class:`wirexfers.providers.tupas.SoloKeyChain`

    Supported return urls:

     * ``cancel`` - user cancels payment
     * ``reject`` - bank rejects payment (due to insufficient funds, ...)
     * ``return`` - payment is successful

    Supported protocol version: ``0003``
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
                  ('CONFIRM', u'NO'),
                  ('KEYVERS', u'0001'),
                  ('CUR', u'EUR')]
        # MAC calculation
        f = lambda x: dict(fields).get(x)
        k = ('VERSION', 'STAMP', 'RCV_ID', 'AMOUNT', 'REF', 'DATE', 'CUR')
        m = '%s&%s&' % ('&'.join(map(f, k)), self.keychain.mac_key)
        fields.append(('MAC', MD5.new(m).hexdigest().upper()))
        return fields
