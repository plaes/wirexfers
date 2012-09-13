# -*- coding: utf-8 -*-
"""
wiretransfers.request
~~~~~~~~~~~~~~~~~~~~~

This module implements a PaymentRequest class which provides us the
payment request forms.
"""
from time import time
from base64 import b64encode

from Crypto.Hash import SHA
from Crypto.Signature import PKCS1_v1_5

class PaymentInfo(object):
    """Payment information required for :class:~`wiretransfers.PaymentRequest`."""
    def __init__(self, amount, message, refnum):
        #: Payment amount as string, uses ``.`` as decimal point separator.
        self.amount = amount
        #: Message used for payment description.
        self.message = message
        #: Reference number.
        self.refnum = refnum

class PaymentRequest(object):
    """PaymentRequest class.

    :param provider: Payment provider
    :type provider: :class:`wiretransfers.providers.ProviderBase`.
    :param info: Payment information
    :type info: :class:`wiretransfers.PaymentInfo`.
    :param return_urls: Dictionary of return URLs. Depends on the specific
                        provider, but generally ``{'return': ... }`` is
                        required.
    :type return_urls: :class:`Dict`

    Raises :exc:`ValueError` when invalid configuration is detected.
    """

    def __init__(self, provider, info, return_urls):
        # TODO: language, payment receiver's account info

        #: :class:`~wiretransfers.providers.ProviderBase` that handles the payment request.
        self.provider = provider

        #: :class:`~wiretransfers.PaymentInfo` containing various payment information (sum, etc..)
        self.info = info

        if 'return' not in return_urls.keys:
            raise ValueError

        #: List containing ``(name, value)`` tuples for HTML form setup.
        self.form = self._sign_form(return_urls)

    def _sign_form(self, return_urls):
        """Create and sign payment request data."""
        # Basic fields
        fields = [('VK_SERVICE', u'1002'),
                  ('VK_VERSION', u'008'),
                  ('VK_SND_ID',  self.provider.user),
                  ('VK_STAMP',   '%d' % int(time())),
                  ('VK_AMOUNT',  self.info.amount),
                  ('VK_CURR',    u'EUR'),
                  ('VK_REF',     self.info.refnum),
                  ('VK_MSG',     self.info.message)]

        ## MAC calculation for request 1002
        mac_fields = ('SERVICE', 'VERSION', 'SND_ID', \
                      'STAMP', 'AMOUNT', 'CURR', 'REF', 'MSG')
        f = lambda x: dict(fields).get('VK_%s' % x)

        mac = u''.join(map(lambda k: '%03d%s' % (len(f(k)), f(k)), mac_fields))
        # Append extra fields
        fields.append(('VK_MAC', b64encode( \
                    PKCS1_v1_5.new(self.provider.private_key).sign(SHA.new(mac)))))
        fields.append(('VK_RETURN', return_urls['return']))
        fields.append(('VK_LANG', 'EST'))
        return fields
