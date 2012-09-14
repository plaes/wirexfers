# -*- coding: utf-8 -*-
"""
wirexfers.provider
~~~~~~~~~~~~~~~~~~

This module contains the payment provider implementations.
"""
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

class LHV(ProviderBase):
    """
    LHV Bank payment protocol provider.

    Homepage: https://www.lhv.ee
    """
