# -*- coding: utf-8 -*-
"""
wirexfers.provider
~~~~~~~~~~~~~~~~~~

This module contains the payment provider implementations.
"""
from time import time
from base64 import b64encode

from Crypto.Hash import SHA
from Crypto.Signature import PKCS1_v1_5

from wirexfers import PaymentRequest

class ProviderBase(object):
    """Base class that all provider implementations derive from."""

    def __init__(self, user, private_key, public_key, endpoint, extra_info={}):

        #: User id for payment processor.
        self.user = user

        #: Endpoint address used to initiate payment requests.
        self.endpoint = endpoint

        #: RSA private key (:py:class:`Crypto.PublicKey.RSA._RSAobj`) object.
        #: See :func:`wirexfers.utils.load_key`.
        self.private_key = private_key

        ##: Private key password
        #self.private_pass = private_pass

        #: RSA public key (:py:class:`Crypto.PublicKey.RSA._RSAobj`) object
        #: See :func:`wirexfers.utils.load_key`.
        self.public_key = public_key

        #: Dictionary containing extra user-supplied information.
        #: Can be used for supplying provider url, etc.
        self.extra_info = extra_info

    def __call__(self, payment, return_urls):
        """
        Creates and returns a payment request.

        :param payment: payment information
        :type payment: :class:`~wirexfers.PaymentInfo`
        :rtype: :class:`~wirexfers.PaymentRequest`
        """
        return PaymentRequest(self, payment, return_urls)

    def parse_response(self, args):
        pass

    def _sign_form(self, info, return_urls):
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
                    PKCS1_v1_5.new(self.private_key).sign(SHA.new(mac)))))
        fields.append(('VK_RETURN', return_urls['return']))
        fields.append(('VK_LANG', 'EST'))
        return fields
