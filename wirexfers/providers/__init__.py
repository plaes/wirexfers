# -*- coding: utf-8 -*-
"""
wirexfers.provider
~~~~~~~~~~~~~~~~~~

This module contains the payment provider implementations.
"""
from wirexfers import PaymentRequest

class KeyChainBase(object):
    """Base class for protocol-specific key handling."""
    def __init__(self):
        raise NotImplementedError('Provider should implement its own keychain.')

class ProviderBase(object):
    """Base class that all provider implementations derive from."""

    def __init__(self, user, keychain, endpoint, extra_info={}):

        #: User id for payment processor.
        self.user = user

        #: Endpoint address used to initiate payment requests.
        self.endpoint = endpoint

        #: Protocol-specific keychain implementation -
        #: :class:`wirexfers.providers.KeyChainBase`
        self.keychain = keychain

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

    def _sign_request(self, info, return_urls):
        """Signs the payment request."""
        raise NotImplementedError('Provider should implement its own signing')
