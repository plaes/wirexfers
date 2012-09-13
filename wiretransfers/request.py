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
    """Payment information required for :class:`wiretransfers.PaymentRequest`."""
    def __init__(self, amount, message, refnum):
        #: Payment amount as string, uses ``.`` as decimal point separator.
        self.amount = amount
        #: Message used for payment description.
        self.message = message
        #: Reference number.
        self.refnum = refnum

class PaymentRequest(object):
    """PaymentRequests class."""

    def __init__(self, provider, payment):
        # TODO: handle return urls, language, payment receiver's account info

        #: Payment provider :class:`wiretransfers.provider.ProviderBase`.
        self.provider = provider

        #: Payment information as :class:`wiretransfers.PaymentInfo`.
        self.payment = payment

        #: List containing ``(name, value)`` tuples for HTML form setup.
        self.form = self._sign_form

    @property
    def _sign_form(self):
        """Create and sign payment request data."""
        # Basic fields
        fields = [('VK_SERVICE', u'1002'),
                  ('VK_VERSION', u'008'),
                  ('VK_SND_ID',  self.provider.user),
                  ('VK_STAMP',   '%d' % int(time())),
                  ('VK_AMOUNT',  self.payment.amount),
                  ('VK_CURR',    u'EUR'),
                  ('VK_REF',     self.payment.refnum),
                  ('VK_MSG',     self.payment.message)]

        ## MAC calculation for request 1002
        mac_fields = ('SERVICE', 'VERSION', 'SND_ID', \
                      'STAMP', 'AMOUNT', 'CURR', 'REF', 'MSG')
        f = lambda x: dict(fields).get('VK_%s' % x)

        mac = u''.join(map(lambda k: '%03d%s' % (len(f(k)), f(k)), mac_fields))
        print mac
        fields.append(('VK_MAC', b64encode( \
                    PKCS1_v1_5.new(self.provider.private_key).sign(SHA.new(mac)))))
        return fields
